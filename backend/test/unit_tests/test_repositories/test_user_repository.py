from app.database.repositories import UserRepository
from app.database.models import User

def test_save_user(user_repository : UserRepository):
    
    user_id = user_repository.save_user(name="Jose",
                              surname="Inverio",
                              telephone="500338659",
                              address="Racławicka 6/52")
    
    added_user = User(
        user_id=user_id ,
        name="Jose",
        surname="Inverio",
        telephone="500338659",
        address="Racławicka 6/52"
    )

    assert added_user.is_equal(user_repository.get_user(user_id=user_id))
    
def test_get_user(user_repository : UserRepository):
    
    user_id = 2
    
    user = user_repository.get_user(user_id=user_id)
    
    assert user.is_equal(User(
        user_id=2,
        name="Jane",
        surname="Smith",
        telephone="987654321",
        address="456 Elm St, Springfield"
    ))

def test_update_user(user_repository : UserRepository):
    
    user_id = 2
    
    data = [{
            "updated_fields" : {
                "address" : "Racławicka 6/4, Kraków"
            }
        }]
    
    user_repository.update_user(user_id=user_id, data=data)
    
    updated_user = user_repository.get_user(user_id=user_id)
    
    assert updated_user.is_equal(User(
        user_id=2,
        name="Jane",
        surname="Smith",
        telephone="987654321",
        address="Racławicka 6/4, Kraków"
    ))

def test_delete_user(user_repository : UserRepository):
    
    user_id = 2
    
    user = user_repository.get_user(user_id=user_id)
    
    assert user.is_equal(User(
        user_id=2,
        name="Jane",
        surname="Smith",
        telephone="987654321",
        address="456 Elm St, Springfield"
    ))
    
    user_repository.delete_user(user_id=user_id)
    
    assert user_repository.get_user(user_id=user_id) == None
    
    
    
    
    