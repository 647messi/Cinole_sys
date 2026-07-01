from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.session import SessionLocal
from app.services.master.raw_material_dict_service import generate_material_code


def generate_codes_for_category(db: Session, category_code: str, times: int = 5) -> list[str]:
    codes = []
    for _ in range(times):
        code = generate_material_code(db=db, material_category_code=category_code)
        codes.append(code)
    return codes


def test_material_code_generation():
    db: Session = SessionLocal()
    try:
        # 保存每个 sequence 当前值
        seq_map = {
            "PRODUCTION": "demo.master.prod_seq",
            "CONSUMABLE": "demo.master.cons_seq",
            "STORAGE": "demo.master.stor_seq",
        }
        original_values = {}
        for cat, seq_name in seq_map.items():
            val = db.execute(text(f"SELECT last_value FROM {seq_name}")).scalar()
            original_values[cat] = val

        categories = ["PRODUCTION", "CONSUMABLE", "STORAGE"]
        all_codes = []

        for category in categories:
            codes = generate_codes_for_category(db, category, times=5)
            all_codes.extend(codes)

            print(f"\n{category}:")
            for code in codes:
                print(f"  {code}")

        unique_count = len(set(all_codes))
        total_count = len(all_codes)

        print("\nSummary:")
        print(f"  Total generated codes: {total_count}")
        print(f"  Unique generated codes: {unique_count}")
        print("  Result:", "PASS - no duplicate codes" if unique_count == total_count else "FAIL - duplicates found")

    finally:
        # 自动复原 sequence
        for cat, seq_name in seq_map.items():
            db.execute(text(f"SELECT setval('{seq_name}', {original_values[cat]})"))
        db.commit()
        db.close()


def test_invalid_category():
    db: Session = SessionLocal()
    try:
        print("\nInvalid category test:")
        try:
            generate_material_code(db=db, material_category_code="INVALID_CATEGORY")
        except Exception as exc:
            print(f"  Result: PASS - error raised: {exc}")
        else:
            print("  Result: FAIL - no error raised")
    finally:
        db.close()


if __name__ == "__main__":
    test_material_code_generation()
    test_invalid_category()
