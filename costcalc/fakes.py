from faker import Faker
import random
from sqlalchemy.exc import IntegrityError
from costcalc.extensions import db
from costcalc.models import User, Material, Labor, Product, ProductMaterial, ProductLabor


fake = Faker('zh_CN')

def fake_users():
    # 创建用户
    users = [
        User(username='xzj', role='admin'),
        User(username='hym', role='admin'),
        User(username='lxp', role='sales'),
        User(username='guest', role='sales'),
    ]
    for user in users:
        user.set_password('123')  # 假设所有用户密码设置为 '123'
    db.session.bulk_save_objects(users)
    db.session.commit()
    user_count = User.query.count()  # 更新用户计数
    print(f"Users created: {user_count}")


# 材料名称词汇表
material_names = [
    "ABS树脂", "聚碳酸酯", "尼龙", "聚苯硫醚", "聚酯",
    "硅胶", "氯丁橡胶", "天然橡胶", "聚丙烯", "聚乙烯",
    "氯化聚乙烯", "聚氯乙烯", "聚苯乙烯", "聚氨酯", "聚四氟乙烯",
    "丁腈橡胶", "氟橡胶", "乙丙橡胶", "热塑性橡胶", "BMC模塑料"
]


# 劳务名称词汇表
labor_names = [
    "切胶分条", "硫化作业", "模压成型", "二次硫化", "拆边工作",
    "修边工作", "质量检验", "产品包装", "注塑成型", "挤出成型",
    "复合挤出", "粉碎回收", "喷涂涂层", "热压成型", "真空成型",
    "旋转成型", "吹塑成型", "发泡成型", "电子束固化", "自动切割"
]

def fake_materials(total_count=20):
    user_count = User.query.count()  # 获取当前数据库中的用户数量
    material_count = total_count // 2  # 由于每个名称生成两个材料，所以这里使用 total_count // 2
    new_materials = []
    
    # 确保每个材料名称生成两个不同规格的材料
    for name in material_names:
        # 生成两个不同规格的材料
        for _ in range(2):  # 固定生成两个实例
            spec = f"{random.randint(10, 100)}厘米"
            new_materials.append(Material(
                name=name,
                user_id=random.randint(1, user_count),
                spec=spec,
                unit_price=random.uniform(1.0, 100.0)
            ))
            if len(new_materials) >= total_count:
                break
        if len(new_materials) >= total_count:
            break

    # 添加到数据库并提交
    for material in new_materials:
        db.session.add(material)
    
    try:
        db.session.commit()
        print(f"{len(new_materials)} materials committed successfully.")
    except IntegrityError as e:
        db.session.rollback()
        print(f"Failed to commit materials due to IntegrityError: {str(e)}")



def fake_labors(count=20):
    user_count = User.query.count()  # 获取当前数据库中的用户数量
    for i in range(count):
        labor = Labor(
            name=labor_names[i],
            user_id=random.randint(1, user_count),
            deprec_cost=fake.random_number(digits=2),
            elec_cost=fake.random_number(digits=2),
            labor_cost=fake.random_number(digits=2)
        )
        db.session.add(labor)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

customer_type_choices = [0.95, 1.0]
payment_term_choices = [1.0, 1.01, 1.02, 1.06]
customer_importance_choices = [1.0, 0.99, 0.98]
estimated_purchase_amount_choices = [1.5, 1.2, 1.1, 1.05, 1.0, 0.99, 0.98, 0.97]
region_price_choices = [0.96, 0.98, 1.0, 1.05, 1.1]
customer_prospect_choices = [1.03, 1.0, 0.98]
product_risk_choices = [1.0, 1.05, 1.15]
technical_quality_requirement_choices = [0.98, 1.0, 1.05, 1.1]
customization_requirement_choices = [0.98, 1.0, 1.03, 1.05]

product_names = [
    "汽车轮胎", "工业输送带", "密封圈", "抗震垫", "橡胶管",
    "电线护套", "橡胶防滑垫", "隔音橡胶", "橡胶手套", "橡胶鞋底",
    "医用导管", "橡胶密封条", "气门嘴", "橡胶球", "橡胶隔膜",
    "防水橡胶布", "耐油橡胶垫", "橡胶接头", "橡胶减震器", "硅胶键盘"
]

def fake_products(count=20):
    user_count = User.query.count()  # 获取当前数据库中的用户数量
    materials = Material.query.all()
    labors = Labor.query.all()
    
    if user_count == 0:
        print("No users available to assign to products.")
        return

    materials = Material.query.all()
    labors = Labor.query.all()
    print(f"Materials available: {len(materials)}, Labors available: {len(labors)}")

    for i in range(count):
        product = Product(
            name=product_names[i % len(product_names)],
            user_id = (i % user_count) + 1,
            trans_method=fake.word(),
            trans_dest=fake.city(),
            trans_cost_kg = round(random.uniform(0.01, 0.1), 2),
            dev_coef=fake.random_number(digits=1),
            fac_coef=fake.random_number(digits=1),
            admin_coef=fake.random_number(digits=1),
            sale_coef=fake.random_number(digits=1),
            finance_coef=fake.random_number(digits=1),
            tax_coef=fake.random_number(digits=1),
            profit_coef=fake.random_number(digits=1),
            customer_type=random.choice(customer_type_choices),
            payment_term=random.choice(payment_term_choices),
            customer_importance=random.choice(customer_importance_choices),
            estimated_purchase_amount=random.choice(estimated_purchase_amount_choices),
            region_price=random.choice(region_price_choices),
            customer_prospect=random.choice(customer_prospect_choices),
            product_risk=random.choice(product_risk_choices),
            technical_quality_requirement=random.choice(technical_quality_requirement_choices),
            customization_requirement=random.choice(customization_requirement_choices)
        )
        selected_materials = random.sample(materials, 2)
        selected_labors = random.sample(labors, 2)

        for mat in selected_materials:
            product_material = ProductMaterial(
                material=mat,
                net_weight=fake.random_number(digits=2),
                gross_weight=fake.random_number(digits=2),
                qualification_rate=fake.random_number(digits=1, fix_len=True) + 0.9  # Generating a float between 0.9 and 1.0
            )
            product.materials.append(product_material)

        for lab in selected_labors:
            product_labor = ProductLabor(
                labor=lab,
                process_time=fake.random_number(digits=3),
                capacity=fake.random_number(digits=1, fix_len=True) + 0.9,
                qualification_rate=fake.random_number(digits=1, fix_len=True) + 0.9  # Generating a float between 0.9 and 1.0
            )
            product.labors.append(product_labor)

        db.session.add(product)
    try:
        db.session.commit()
        print("Products committed successfully.")
    except IntegrityError:
        db.session.rollback()
        print(f"Failed to commit products: {str(e)}")


