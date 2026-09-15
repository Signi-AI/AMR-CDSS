from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.models.user import Role
from app.core.database import get_db



router = APIRouter(
    tags=["SEED"]
)


roles = [
    {
        "name":"doctor"
    },{
        "name":"admin"
    }
]


@router.post("/seed")
def see_roles(db:Session=Depends(get_db)):



    add_any = False
    for role in roles:
        exists = (
            db.query(Role).filter(Role.name == role["name"])
        ).first()

        if not exists:
            db.add(Role(**role))
            add_any = True

    db.commit()

    if add_any:
        return{"message":"role seeded successfuly"}

    return{"message": "seed already planted"}    
 



