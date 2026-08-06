class UserService:
    def __init__(self, repository):
        self.repo = repository

    def get_all_users(self):
        users = self.repo.get_all_users()
        return {"message": "Users retrieved successfully", "data": users}

    def get_user_by_id(self, user_id: int):
        user = self.repo.get_user_by_id(user_id)
        if not user:
            return None
        return {"message": "User retrieved successfully", "data": user}

    def create_user(self, user_data: dict):
        user = self.repo.create_user(user_data)
        return {"message": "User created successfully", "data": user}

    def update_user(self, user_id: int, user_data: dict):
        user = self.repo.update_user(user_id, user_data)
        if not user:
            return None
        return {"message": "User updated successfully", "data": user}

    def delete_user(self, user_id: int):
        deleted = self.repo.delete_user(user_id)
        if not deleted:
            return None
        return {"message": "User deleted successfully"}