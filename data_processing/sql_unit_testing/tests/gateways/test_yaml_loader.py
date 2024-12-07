from project.gateways.yaml_loader import YAMLLoader

def test_yaml_loader_load_yaml():
    file_path = "tests/gateways/files/test_yaml_loader.yaml"
    loader = YAMLLoader()
    dict_from_file = loader.load_dict_from_yaml(file_path)

    expected_dict = {"a": {"b": ["c","d"]}}

    assert dict_from_file == expected_dict
