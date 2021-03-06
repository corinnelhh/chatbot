from fabric.api import run
from fabric.api import env
from fabric.api import prompt
from fabric.api import execute
from fabric.api import sudo
from fabric import contrib
from fabric.contrib.project import rsync_project
import boto.ec2
import time
import boto

env.hosts = ['localhost', ]
env.aws_region = 'us-west-2'


def host_type():
    run('uname -s')


def get_ec2_connection():
    if 'ec2' not in env:
        conn = boto.ec2.connect_to_region(env.aws_region)
        if conn is not None:
            env.ec2 = conn
            print "Connected to EC2 region %s" % env.aws_region
        else:
            msg = "Unable to connect to EC2 region %s"
            raise IOError(msg % env.aws_region)
    return env.ec2


def provision_instance(wait_for_running=False, timeout=120, interval=2):
    wait_val = int(interval)
    timeout_val = int(timeout)
    conn = get_ec2_connection()
    instance_type = 'm3.medium'
    key_name = 'pk-aws'
    security_group = 'ssh-access'
    image_id = 'ami-d0d8b8e0'

    reservations = conn.run_instances(
        image_id,
        key_name=key_name,
        instance_type=instance_type,
        security_groups=[security_group, ]
    )
    new_instances = [
        i for i in reservations.instances if i.state == u'pending'
    ]
    running_instance = []
    if wait_for_running:
        waited = 0
        while new_instances and (waited < timeout_val):
            time.sleep(wait_val)
            waited += int(wait_val)
            for instance in new_instances:
                state = instance.state
                print "Instance %s is %s" % (instance.id, state)
                if state == "running":
                    running_instance.append(
                        new_instances.pop(new_instances.index(i))
                    )
                instance.update()


def list_aws_instances(verbose=False, state='all'):
    conn = get_ec2_connection()

    reservations = conn.get_all_reservations()
    instances = []
    for res in reservations:
        for instance in res.instances:
            if state == 'all' or instance.state == state:
                instance = {
                    'id': instance.id,
                    'type': instance.instance_type,
                    'image': instance.image_id,
                    'state': instance.state,
                    'instance': instance,
                }
                instances.append(instance)
    env.instances = instances
    if verbose:
        import pprint
        pprint.pprint(env.instances)


def select_instance(state='running'):
    if env.get('active_instance', False):
        return

    list_aws_instances(state=state)

    prompt_text = "Please select from the following instances:\n"
    instance_template = " %(ct)d: %(state)s instance %(id)s\n"
    for idx, instance in enumerate(env.instances):
        ct = idx + 1
        args = {'ct': ct}
        args.update(instance)
        prompt_text += instance_template % args
    prompt_text += "Choose an instance: "

    def validation(input):
        choice = int(input)
        if choice not in range(1, len(env.instances) + 1):
            raise ValueError("%d is not a valid instance" % choice)
        return choice

    choice = prompt(prompt_text, validate=validation)
    env.active_instance = env.instances[choice - 1]['instance']


def run_command_on_selected_server(command, *args, **kwargs):
    select_instance()
    selected_hosts = [
        'ubuntu@' + env.active_instance.public_dns_name
    ]
    kwargs['hosts'] = selected_hosts
    execute(command, *args, **kwargs)


def _install_nginx():
    sudo('apt-get --yes install nginx')
    print "installed nginx"
    sudo('/etc/init.d/nginx start')


def install_nginx():
    run_command_on_selected_server(_install_nginx)


def _install_supervisor():
    sudo('apt-get --yes install supervisor')
    print "installed supervisor"
    sudo('mv ./chatbot/supervisord.conf /etc/supervisor/conf.d/chatbot.conf')
    sudo('/etc/init.d/supervisor stop')
    sudo('/etc/init.d/supervisor start')


def install_supervisor():
    run_command_on_selected_server(_install_supervisor)


def _move_nginx_files():
    sudo('mv /etc/nginx/sites-available/default \
        /etc/nginx/sites-available/default.orig')
    sudo('mv ./chatbot/simple_nginx_config /etc/nginx/sites-available/default')
    sudo('/etc/init.d/nginx restart')
    # sudo('python ./chatbot/chatbot.py')


def move_nginx_files():
    run_command_on_selected_server(_move_nginx_files)


def _install_flask():
    sudo ('apt-get --yes install python-pip')
    sudo ('pip install flask')
    sudo ('pip install nltk')
    # sudo ('pip install numpy')


def install_flask():
    run_command_on_selected_server(_install_flask)


def stop_instance():
    conn = get_ec2_connection()
    select_instance('running')
    conn.stop_instances(env.active_instance.id)


def terminate_instance():
    conn = get_ec2_connection()
    select_instance('stopped')
    conn.terminate_instances(env.active_instance.id)


def update_apt():
    sudo("apt-get update")


def install_numpy():
    sudo("apt-get install python-numpy")


def move_nltk_file():
    sudo("mv chatbot/nltk_data/ ~/")


def generate_nginx_config():
    config_file = """
server {
    listen 80;
    server_name http://%s/;
    access_log  /var/log/nginx/test.log;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}""" % env.active_instance.public_dns_name
    with open("simple_nginx_config", 'w') as outfile:
        outfile.write(config_file)


def deploy():
    list_aws_instances()
    not_running = True
    while not_running:
        for instance in env.instances:
            if instance['state'] == u'running':
                not_running = False
        list_aws_instances()
    run_command_on_selected_server(update_apt)
    run_command_on_selected_server(install_numpy)
    install_nginx()
    generate_nginx_config()
    run_command_on_selected_server(rsync_project, remote_dir="~/", exclude=[".git"])
    #run_command_on_selected_server(move_nltk_file)
    install_flask()
    install_supervisor()
    move_nginx_files()
