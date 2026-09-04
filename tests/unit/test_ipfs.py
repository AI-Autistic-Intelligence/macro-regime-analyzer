from src.storage.ipfs import IPFSManager


def test_ipfs_manager(tmpdir):
    manager = IPFSManager()
    
    # Create a dummy file
    dummy_file = tmpdir.join("dummy_model.bin")
    dummy_file.write("test model weights")
    
    # Test upload (mock)
    cid = manager.upload_file(str(dummy_file))
    assert cid == "QmTestMockCid123456789"
    
    # Test download (mock)
    output_file = tmpdir.join("downloaded_model.bin")
    success = manager.download_file(cid, str(output_file))
    
    assert success is True
    assert output_file.read() == "mock model data"
