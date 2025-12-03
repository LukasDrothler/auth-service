import pytest
from src.user_queries import (
    get_user_by_email, 
    get_user_by_id, 
    get_user_by_username,
    create_user,
    update_user_last_seen,
    delete_user
)
from src.database_service import DatabaseService
import uuid
from datetime import datetime

def test_database_connection(db_service: DatabaseService):
    """Test that the database service can connect and execute queries"""
    assert db_service.db_connection_works() is True
    assert db_service.database == "auth_test"

def test_create_and_get_user(db_service: DatabaseService):
    """Test creating a user and retrieving it via queries"""
    username = "testuser"
    email = "test@example.com"
    hashed_password = "hashed_secret"
    
    # Test create_user
    create_user(username, email, hashed_password, db_service)
    
    # Test get_user_by_email
    user = get_user_by_email(email, db_service)
    assert user is not None
    assert user.username == username
    assert user.email == email
    
    # Test get_user_by_id
    user_by_id = get_user_by_id(user.id, db_service)
    assert user_by_id is not None
    assert user_by_id.email == email
    
    # Test get_user_by_username
    user_by_username = get_user_by_username(username, db_service)
    assert user_by_username is not None
    assert user_by_username.id == user.id

def test_update_user_last_seen(db_service: DatabaseService):
    """Test updating user's last seen timestamp"""
    username = "update_test"
    email = "update@example.com"
    hashed_password = "hashed_secret"
    
    create_user(username, email, hashed_password, db_service)
    user = get_user_by_email(email, db_service)
    
    assert user.last_seen is None
    
    update_user_last_seen(user.id, db_service)
    
    updated_user = get_user_by_id(user.id, db_service)
    assert updated_user.last_seen is not None
    assert isinstance(updated_user.last_seen, datetime)

def test_delete_user(db_service: DatabaseService):
    """Test deleting a user"""
    username = "delete_test"
    email = "delete@example.com"
    hashed_password = "hashed_secret"
    
    create_user(username, email, hashed_password, db_service)
    user = get_user_by_email(email, db_service)
    assert user is not None
    
    delete_user(user.id, db_service)
    
    deleted_user = get_user_by_id(user.id, db_service)
    assert deleted_user is None

