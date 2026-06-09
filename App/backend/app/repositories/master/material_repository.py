from sqlalchemy import text
from sqlalchemy.orm import Session
from app.models.master.material_model import Material


def get_all_materials(db: Session) -> list[Material]:
    return (
        db.query(Material)
        .order_by(Material.id.desc())
        .all()
    )


def get_material_by_id(db: Session, material_id: int) -> Material | None:
    return (
        db.query(Material)
        .filter(Material.id == material_id)
        .first()
    )


def get_material_by_code(db: Session, material_code: str) -> Material | None:
    return (
        db.query(Material)
        .filter(Material.material_code == material_code)
        .first()
    )


def get_materials_by_category(
    db: Session,
    category_code: str,
) -> list[Material]:
    return (
        db.query(Material)
        .filter(Material.material_category_code == category_code)
        .order_by(Material.id.desc())
        .all()
    )


def create_material(db: Session, material: Material) -> Material:
    db.add(material)
    db.commit()
    db.refresh(material)

    return material


def update_material(db: Session, material: Material) -> Material:
    db.commit()
    db.refresh(material)

    return material

#------------------- Additional helper functions ------------------#

# 生成物料编码，格式：MAT-{分类代码}-{3位序列号}

def get_next_material_sequence(db: Session, category_code: str) -> int:
    """
    根据分类调用数据库 sequence 获取下一个值
    """
    sequence_map = {
        "PRODUCTION": "demo.master.prod_seq",
        "CONSUMABLE": "demo.master.cons_seq",
        "STORAGE": "demo.master.stor_seq",
    }


    seq_name = sequence_map.get(category_code.upper())
    if not seq_name:
        raise ValueError(f"Unsupported category_code: {category_code}")

    result = db.execute(text(f"SELECT nextval('{seq_name}')")).scalar()
    return result