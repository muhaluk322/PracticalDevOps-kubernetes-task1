from conftest import DATA
import pytest


@pytest.mark.parametrize('obj', DATA)
def test_allowed_kind_values(obj: dict):
    assert obj['kind'] in ('Deployment', 'Service')


@pytest.mark.parametrize(
    'obj',
    filter(lambda x: x['kind'] == 'Service', DATA)
)
def test_service_type(obj: dict):
    assert obj['spec']['type'] == 'NodePort'

@pytest.mark.parametrize(
    'obj',
    filter(lambda x: x['kind'] == 'Service', DATA)
)
def test_service_selector(obj: dict):
    assert obj['spec']['selector']['app'] == 'wordpress'

@pytest.mark.parametrize(
    'obj',
    filter(lambda x: x['kind'] == 'Service', DATA)
)
def test_service_port(obj: dict):
    assert obj['spec']['ports'][0]['port'] == 80

@pytest.mark.parametrize(
    'obj',
    filter(lambda x: x['kind'] == 'Service', DATA)
)
def test_service_target(obj: dict):
    assert obj['spec']['ports'][0]['targetPort'] == 80

@pytest.mark.parametrize(
    'obj',
    filter(lambda x: x['kind'] == 'Service', DATA)
)
def test_service_node(obj: dict):
    assert obj['spec']['ports'][0]['nodePort'] == 31000

@pytest.mark.parametrize(
    'obj',
    filter(lambda x: x['kind'] == 'Deployment', DATA)
)
def test_deployment_selector(obj: dict):
    assert obj['spec']['selector']['matchLabels']['app'] == 'wordpress'

@pytest.mark.parametrize(
    'obj',
    filter(lambda x: x['kind'] == 'Deployment', DATA)
)
def test_deployment_labels(obj: dict):
    assert obj['spec']['template']['metadata']['labels']['app'] == 'wordpress'

@pytest.mark.parametrize(
    'obj',
    filter(lambda x: x['kind'] == 'Deployment', DATA)
)
def test_deployment_container_name(obj: dict):
    containers = obj['spec']['template']['spec']['containers']
    wordpress = list(filter(lambda c: c['name'] == 'wordpress', containers))
    assert len(wordpress) == 1

@pytest.mark.parametrize(
    'obj',
    filter(lambda x: x['kind'] == 'Deployment', DATA)
)
def test_deployment_container_image(obj: dict):
    containers = obj['spec']['template']['spec']['containers']
    wordpress = list(filter(lambda c: c['name'] == 'wordpress', containers))[0]
    assert wordpress['image'] == 'wordpress'

@pytest.mark.parametrize(
    'obj',
    filter(lambda x: x['kind'] == 'Deployment', DATA)
)
def test_deployment_container_env_host(obj: dict):
    containers = obj['spec']['template']['spec']['containers']
    wordpress = list(filter(lambda c: c['name'] == 'wordpress', containers))[0]
    host = list(filter(lambda c: c['name'] == 'WORDPRESS_DB_HOST', wordpress['env']))[0]
    assert host['value'] == 'mysql'

@pytest.mark.parametrize(
    'obj',
    filter(lambda x: x['kind'] == 'Deployment', DATA)
)
def test_deployment_container_env_secret_name(obj: dict):
    containers = obj['spec']['template']['spec']['containers']
    wordpress = list(filter(lambda c: c['name'] == 'wordpress', containers))[0]
    password = list(filter(lambda c: c['name'] == 'WORDPRESS_DB_PASSWORD', wordpress['env']))[0]
    assert password['valueFrom']['secretKeyRef']['name'] == 'sql-pass'

@pytest.mark.parametrize(
    'obj',
    filter(lambda x: x['kind'] == 'Deployment', DATA)
)
def test_deployment_container_env_secret_key(obj: dict):
    containers = obj['spec']['template']['spec']['containers']
    wordpress = list(filter(lambda c: c['name'] == 'wordpress', containers))[0]
    password = list(filter(lambda c: c['name'] == 'WORDPRESS_DB_PASSWORD', wordpress['env']))[0]
    assert password['valueFrom']['secretKeyRef']['key'] == 'password'

@pytest.mark.parametrize(
    'obj',
    filter(lambda x: x['kind'] == 'Deployment', DATA)
)
def test_deployment_container_port(obj: dict):
    containers = obj['spec']['template']['spec']['containers']
    wordpress = list(filter(lambda c: c['name'] == 'wordpress', containers))[0]
    port = list(filter(lambda c: c['containerPort'] == 80, wordpress['ports']))
    assert len(port) == 1
