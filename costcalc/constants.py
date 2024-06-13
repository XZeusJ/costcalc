# constants.py

# 客户类型
CUSTOMER_TYPE_MAPPING = {
    0.95: '新客户',
    1.0: '老客户'
}

# 客户账期
PAYMENT_TERM_MAPPING = {
    1.0: '款到发货',
    1.01: '及时月结',
    1.02: '及时3月结',
    1.06: '不及时月结'
}

# 客户重要程度
CUSTOMER_IMPORTANCE_MAPPING = {
    1.0: '一般',
    0.99: '重要',
    0.98: '很重要'
}

# 此产品预计采购金额
ESTIMATED_PURCHASE_AMOUNT_MAPPING = {
    1.5: '1000以下',
    1.2: '3000以下',
    1.1: '5000以下',
    1.05: '5000-1万',
    1.0: '1万-5万',
    0.99: '5万以上',
    0.98: '15万以上',
    0.97: '30万以上'
}

# 客户区域价格
REGION_PRICE_MAPPING = {
    0.96: '极低',
    0.98: '低',
    1.0: '中',
    1.05: '高',
    1.1: '极高'
}

# 客户前景
CUSTOMER_PROSPECT_MAPPING = {
    1.03: '新兴行业',
    1.0: '传统行业',
    0.98: '市场竞争激烈'
}

# 产品风险
PRODUCT_RISK_MAPPING = {
    1.0: '无风险',
    1.05: '中风险',
    1.15: '高风险'
}

# 产品技术及品质要求
TECHNICAL_QUALITY_REQUIREMENT_MAPPING = {
    0.98: '无要求',
    1.0: '普通',
    1.05: '较高',
    1.1: '高'
}

# 产品是否特殊定制
CUSTOMIZATION_REQUIREMENT_MAPPING = {
    0.98: '通用件标准件',
    1.0: '一般',
    1.03: '特殊仅几家用',
    1.05: '独家'
}
