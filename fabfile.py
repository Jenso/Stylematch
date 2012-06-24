from fabric.api import sudo, env, cd, run
from fabric.contrib.console import confirm
import datetime

# production server, expects accepted ssh key on server
try:
    from fabsettings import host
    env.hosts = host
except:
    env.hosts = ['proxz@stylematch.se']
env.directory = '/home/ubuntu/ProjectX'
env.activate = 'source /home/ubuntu/ProjectX/projectx/bin/activate'
env.deploy_user = 'ubuntu'

"""
TODO: Write local deploy script with local()
instead of current bash script.
"""


def virtualenv(command):
    """
    Execute commands in virtualenv, as env.deploy_user
    """
    with cd(env.directory):
        sudo(env.activate + '&&' + command, user=env.deploy_user)


def git_pull():
    'Updates the repository.'
    with cd(env.directory):
        sudo('git pull', user=env.deploy_user)


def update_dependencies():
    virtualenv("pip install -r requirements.txt")


def upload_static_files():
    virtualenv("./manage.py collectstatic --noinput")


def compile_less():
    virtualenv("lessc bootstrap/static/less/bootstrap.less "
                     "bootstrap/static/css/style.css")


def backup_database():
    now = datetime.datetime.now()
    filename = ("/home/ubuntu/database_backup/stylematchdb_"
                + now.strftime("%y%m%d-%H-%M") + ".sql")
    sudo("mysqldump -u root -p django_stylematch > " + filename)


def migrate_db():
    virtualenv("./manage.py migrate accounts")

def restart_nginx():
    sudo("/etc/init.d/nginx restart")


def top():
    sudo("top")


def update_git_submodules():
    with cd(env.directory):
        sudo('git submodule init', user=env.deploy_user)
        sudo('git submodule update', user=env.deploy_user)


def restart_gunicorn():
    sudo("restart django_stylematch")


def deploy_db_change():
    update_dependencies()
    backup_database()
    git_pull()
    update_git_submodules()
    migrate_db()
    compile_less()
    upload_static_files()
    restart_gunicorn()


def deploy():
    update_dependencies()
    git_pull()
    update_git_submodules()
    compile_less()
    upload_static_files()
    restart_gunicorn()
