import os

# Mock function for file operations (to be replaced with actual implementation)
def mock_sync(source_folder, replica_folder, log_file):
    pass

# Testing one-way synchronization - new text file
def test_one_way_sync(tmp_path):
    source_folder = tmp_path / "source"
    replica_folder = tmp_path / "replica"
    log_file = tmp_path / "sync.log"

    try:
        os.makedirs(source_folder)
    except OSError as error:
        print(error)
        
    try: 
        with open(source_folder / "file.txt", "w") as f:
            f.write("Source content")
    except OSError as error:
        print(error)
    finally:
        f.close()   

    mock_sync(source_folder, replica_folder, log_file)

    assert os.path.exists(replica_folder / "file.txt")
    with open(replica_folder / "file.txt", "r") as f:
        assert f.read() == "Source content"