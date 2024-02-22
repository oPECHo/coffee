import sys
import mongoengine as me
from coffee import models
import datetime
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def check_has_user_admin_and_reset_pwd():
    print("Checking has user admin")
    user = models.User.objects(username="admin").first()
    if user:
        user.set_password("p@ssw0rd")
        user.save()
        print("There is a user admin.\nReset admin password: Done")
        return True
    return False


def create_user_admin():
    print("start create admin")
    user = models.User(
        username="admin",
        first_name="admin",
        last_name="system",
        email="admin@example.com",
        roles=["user", "admin"],
    )
    user.set_password("p@ssw0rd")
    user.save()
    print("finish")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        me.connect(db="coffeedb", host=sys.argv[1])
    else:
        me.connect(db="coffeedb")
    print("start create")
    if not check_has_user_admin_and_reset_pwd():
        create_user_admin()

    print("end create")
