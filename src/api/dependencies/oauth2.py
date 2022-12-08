# class RoleChecker:
#     def __init__(self, allowed_roles: list):
#         self.allowed_roles = allowed_roles

#     def __call__(self, user: User = Depends(get_current_active_user)):
#         if user.role not in self.allowed_roles:
#             logger.debug(f"User with role {user.role} not in {self.allowed_roles}")
#             raise HTTPException(status_code=403, detail="Operation not permitted")