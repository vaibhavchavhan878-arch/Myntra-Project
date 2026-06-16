# ============================================
#   GrowthCipher — Sales & Revenue Analytics
#   Company Theme: Myntra (Fashion & Lifestyle)
#   Step 4: Python EDA + Revenue Forecasting
#   Tool: VS Code
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pyodbc
import warnings
from sklearn.linear_model import LinearRegression
warnings.filterwarnings('ignore')

# Myntra Brand Colors
MYNTRA_PINK  = '#FF3F6C'
MYNTRA_NAVY  = '#282C3F'
MYNTRA_GREY  = '#F0F0F0'
MYNTRA_LIGHT = '#FFB6C1'

plt.rcParams['figure.figsize'] = (12, 5)
sns.set_style('whitegrid')

# ============================================
# STEP 1 — SQL Server se Data Load karo
# ============================================
print("📦 Data load ho raha hai...")

conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=LAPTOP-RGU7T970\MSSQLSERVER2025;'
    'DATABASE=growthcipher_myntra;'
    'Trusted_Connection=yes;'
)

orders      = pd.read_sql('SELECT * FROM orders',      conn)
order_items = pd.read_sql('SELECT * FROM order_items', conn)
customers   = pd.read_sql('SELECT * FROM customers',   conn)
products    = pd.read_sql('SELECT * FROM products',    conn)
brands      = pd.read_sql('SELECT * FROM brands',      conn)
regions     = pd.read_sql('SELECT * FROM regions',     conn)
conn.close()

print(f"✅ Data load ho gaya!")
print(f"   Orders      : {len(orders)} rows")
print(f"   Order Items : {len(order_items)} rows")
print(f"   Customers   : {len(customers)} rows")

# ============================================
# STEP 2 — Data Cleaning
# ============================================
print("\n🧹 Data clean ho raha hai...")

orders['order_date']     = pd.to_datetime(orders['order_date'])
orders['delivery_date']  = pd.to_datetime(orders['delivery_date'])
customers['joined_date'] = pd.to_datetime(customers['joined_date'])

print(f"   Null values  — Orders      : {orders.isnull().sum().sum()}")
print(f"   Null values  — Order Items : {order_items.isnull().sum().sum()}")
print(f"   Duplicates   — Orders      : {orders.duplicated().sum()}")
print(f"   Duplicates   — Order Items : {order_items.duplicated().sum()}")

# Revenue column calculate karo
order_items['revenue'] = (
    order_items['quantity'] *
    order_items['unit_price'] *
    (1 - order_items['discount'] / 100)
)

# Master dataframe banao
df = order_items \
    .merge(orders,    on='order_id') \
    .merge(products,  on='product_id') \
    .merge(brands,    on='brand_id') \
    .merge(customers, on='customer_id') \
    .merge(regions,   on='region_id')

df['order_month'] = df['order_date'].dt.to_period('M')
df['month_name']  = df['order_date'].dt.strftime('%b %Y')

print(f"✅ Master dataframe ready! Rows: {len(df)}, Columns: {len(df.columns)}")

# ============================================
# STEP 3 — Key Business Metrics
# ============================================
total_revenue   = df['revenue'].sum()
total_orders    = df['order_id'].nunique()
total_customers = df['customer_id'].nunique()
avg_order_value = total_revenue / total_orders
total_units     = df['quantity'].sum()

print("\n" + "=" * 45)
print("   GrowthCipher — Key Business Metrics")
print("=" * 45)
print(f"  Total Revenue     : Rs.{total_revenue:,.2f}")
print(f"  Total Orders      : {total_orders}")
print(f"  Total Customers   : {total_customers}")
print(f"  Avg Order Value   : Rs.{avg_order_value:,.2f}")
print(f"  Total Units Sold  : {total_units}")
print("=" * 45)

# ============================================
# STEP 4 — Monthly Revenue Trend Chart
# ============================================
print("\n📊 Charts ban rahe hain...")

monthly_rev = df.groupby('order_month')['revenue'].sum().reset_index()
monthly_rev['order_month'] = monthly_rev['order_month'].astype(str)

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(monthly_rev['order_month'], monthly_rev['revenue'],
        color=MYNTRA_PINK, linewidth=2.5, marker='o', markersize=7)
ax.fill_between(monthly_rev['order_month'], monthly_rev['revenue'],
                alpha=0.15, color=MYNTRA_PINK)

for i, row in monthly_rev.iterrows():
    ax.annotate(f"Rs.{row['revenue']/1000:.0f}K",
                (row['order_month'], row['revenue']),
                textcoords='offset points', xytext=(0, 10),
                ha='center', fontsize=8, color=MYNTRA_NAVY)

ax.set_title('Monthly Revenue Trend — Myntra GrowthCipher',
             fontsize=14, fontweight='bold', color=MYNTRA_NAVY, pad=15)
ax.set_xlabel('Month', fontsize=11)
ax.set_ylabel('Revenue (Rs.)', fontsize=11)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'Rs.{x/1000:.0f}K'))
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('monthly_revenue_trend.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ monthly_revenue_trend.png saved!")

# ============================================
# STEP 5 — Top 5 Products by Revenue
# ============================================
top_products = df.groupby('product_name')['revenue'] \
                 .sum().nlargest(5).reset_index()

fig, ax = plt.subplots(figsize=(12, 5))
bars = ax.barh(top_products['product_name'], top_products['revenue'],
               color=MYNTRA_PINK, edgecolor='white')

for bar, val in zip(bars, top_products['revenue']):
    ax.text(val + 300, bar.get_y() + bar.get_height()/2,
            f'Rs.{val:,.0f}', va='center', fontsize=9, color=MYNTRA_NAVY)

ax.set_title('Top 5 Products by Revenue',
             fontsize=14, fontweight='bold', color=MYNTRA_NAVY, pad=15)
ax.set_xlabel('Revenue (Rs.)', fontsize=11)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('top5_products.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ top5_products.png saved!")

# ============================================
# STEP 6 — Top 5 Brands by Revenue
# ============================================
top_brands = df.groupby('brand_name')['revenue'] \
               .sum().nlargest(5).reset_index()

colors = [MYNTRA_PINK, MYNTRA_NAVY, '#FF7096', '#4A5568', MYNTRA_LIGHT]
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(top_brands['brand_name'], top_brands['revenue'],
              color=colors, edgecolor='white', width=0.5)

for bar, val in zip(bars, top_brands['revenue']):
    ax.text(bar.get_x() + bar.get_width()/2, val + 300,
            f'Rs.{val:,.0f}', ha='center', fontsize=9, color=MYNTRA_NAVY)

ax.set_title('Top 5 Brands by Revenue',
             fontsize=14, fontweight='bold', color=MYNTRA_NAVY, pad=15)
ax.set_ylabel('Revenue (Rs.)', fontsize=11)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'Rs.{x/1000:.0f}K'))
plt.tight_layout()
plt.savefig('top5_brands.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ top5_brands.png saved!")

# ============================================
# STEP 7 — Category & Gender Analysis
# ============================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

cat_rev = df.groupby('category')['revenue'].sum()
axes[0].pie(cat_rev, labels=cat_rev.index, autopct='%1.1f%%',
            colors=[MYNTRA_PINK, MYNTRA_NAVY],
            startangle=90, wedgeprops={'edgecolor': 'white', 'linewidth': 2})
axes[0].set_title('Men vs Women Revenue Split',
                  fontsize=13, fontweight='bold', color=MYNTRA_NAVY)

city_gender = df.groupby(['city', 'gender'])['revenue'].sum().unstack()
city_gender.plot(kind='bar', ax=axes[1],
                 color=[MYNTRA_PINK, MYNTRA_NAVY],
                 edgecolor='white', width=0.6)
axes[1].set_title('City wise Revenue by Gender',
                  fontsize=13, fontweight='bold', color=MYNTRA_NAVY)
axes[1].set_xlabel('City', fontsize=10)
axes[1].set_ylabel('Revenue (Rs.)', fontsize=10)
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'Rs.{x/1000:.0f}K'))
axes[1].legend(title='Gender')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('demographics_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ demographics_analysis.png saved!")

# ============================================
# STEP 8 — Payment Mode & Region Analysis
# ============================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

payment = df.groupby('payment_mode')['order_id'].nunique()
axes[0].pie(payment, labels=payment.index, autopct='%1.1f%%',
            colors=[MYNTRA_PINK, MYNTRA_NAVY, MYNTRA_LIGHT, '#4A5568'],
            startangle=90, wedgeprops={'edgecolor': 'white', 'linewidth': 2})
axes[0].set_title('Payment Mode Split',
                  fontsize=13, fontweight='bold', color=MYNTRA_NAVY)

region_rev = df.groupby('city')['revenue'].sum().sort_values(ascending=True)
axes[1].barh(region_rev.index, region_rev.values,
             color=MYNTRA_PINK, edgecolor='white')
axes[1].set_title('City wise Revenue',
                  fontsize=13, fontweight='bold', color=MYNTRA_NAVY)
axes[1].set_xlabel('Revenue (Rs.)', fontsize=10)
axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'Rs.{x/1000:.0f}K'))
plt.tight_layout()
plt.savefig('payment_region_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ payment_region_analysis.png saved!")

# ============================================
# STEP 9 — Revenue Forecasting (Next 3 Months)
# ============================================
print("\n🔮 Revenue forecast calculate ho raha hai...")

monthly = df.groupby('order_month')['revenue'].sum().reset_index()
monthly['month_num'] = range(1, len(monthly) + 1)

X = monthly[['month_num']]
y = monthly['revenue']
model = LinearRegression()
model.fit(X, y)

last_month     = len(monthly)
future_months  = pd.DataFrame({'month_num': [last_month+1, last_month+2, last_month+3]})
forecast       = model.predict(future_months)
last_date      = df['order_date'].max()
future_labels  = [
    (last_date + pd.DateOffset(months=i)).strftime('%b %Y')
    for i in range(1, 4)
]

print("=" * 40)
print("   Revenue Forecast — Next 3 Months")
print("=" * 40)
for label, rev in zip(future_labels, forecast):
    print(f"   {label}  ->  Rs.{rev:,.2f}")
print("=" * 40)

# Forecast Chart
fig, ax = plt.subplots(figsize=(14, 5))

ax.plot(monthly['order_month'].astype(str), monthly['revenue'],
        color=MYNTRA_PINK, linewidth=2.5, marker='o',
        markersize=7, label='Actual Revenue')
ax.fill_between(monthly['order_month'].astype(str), monthly['revenue'],
                alpha=0.15, color=MYNTRA_PINK)

connect_months  = [monthly['order_month'].astype(str).iloc[-1]] + future_labels
connect_revenue = [monthly['revenue'].iloc[-1]] + list(forecast)
ax.plot(connect_months, connect_revenue,
        color=MYNTRA_NAVY, linewidth=2.5, marker='s',
        markersize=8, linestyle='--', label='Forecasted Revenue')

for label, rev in zip(future_labels, forecast):
    ax.annotate(f'Rs.{rev/1000:.0f}K',
                (label, rev), textcoords='offset points',
                xytext=(0, 12), ha='center', fontsize=9,
                color=MYNTRA_NAVY, fontweight='bold')

ax.set_title('Revenue Forecast — Next 3 Months (Linear Regression)',
             fontsize=14, fontweight='bold', color=MYNTRA_NAVY, pad=15)
ax.set_xlabel('Month', fontsize=11)
ax.set_ylabel('Revenue (Rs.)', fontsize=11)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'Rs.{x/1000:.0f}K'))
ax.legend(fontsize=10)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('revenue_forecast.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ revenue_forecast.png saved!")

# ============================================
# STEP 10 — Final Business Insights Summary
# ============================================
top_product  = df.groupby('product_name')['revenue'].sum().idxmax()
top_brand    = df.groupby('brand_name')['revenue'].sum().idxmax()
top_city     = df.groupby('city')['revenue'].sum().idxmax()
top_payment  = df.groupby('payment_mode')['order_id'].nunique().idxmax()
top_category = df.groupby('category')['revenue'].sum().idxmax()

print("\n" + "=" * 50)
print("   GrowthCipher — Final Business Insights")
print("=" * 50)
print(f"  Total Revenue     : Rs.{total_revenue:,.2f}")
print(f"  Total Orders      : {total_orders}")
print(f"  Total Customers   : {total_customers}")
print(f"  Top Product       : {top_product}")
print(f"  Top Brand         : {top_brand}")
print(f"  Top City          : {top_city}")
print(f"  Top Payment Mode  : {top_payment}")
print(f"  Top Category      : {top_category}")
print()
print("  Next 3 Months Forecast:")
for label, rev in zip(future_labels, forecast):
    print(f"     {label}  ->  Rs.{rev:,.2f}")
print("=" * 50)
print("\n✅ GrowthCipher Analysis Complete!")