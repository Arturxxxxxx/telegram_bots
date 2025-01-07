def generate_report(data):
    total_sales = sum(item.get("totalPrice", 0) for item in data)
    total_items = len(data)
    total_discounts = sum((item.get("discountPercent", 0) / 100) * item.get("totalPrice", 0) for item in data)
    total_commission = sum((item.get("spp", 0) / 100) * item.get("totalPrice", 0) for item in data)
    total_payment_sale_amount = sum(item.get("paymentSaleAmount", 0) for item in data)
    total_logistics = sum(item.get("finishedPrice", 0) - item.get("priceWithDisc", 0) for item in data)

    average_sale_price = total_sales / total_items if total_items else 0

    report = (
        f"Отчет по продажам:\n"
        f"- **Общая сумма продаж:** {total_sales:,.2f} руб.\n"
        f"- **Количество проданных единиц:** {total_items}\n"
        f"- **Сумма скидок:** {total_discounts:,.2f} руб.\n"
        f"- **Комиссия Wildberries:** {total_commission:,.2f} руб.\n"
        f"- **Оплата за продажу:** {total_payment_sale_amount:,.2f} руб.\n"
        f"- **Стоимость логистики:** {total_logistics:,.2f} руб.\n"
        f"- **Средняя цена продажи:** {average_sale_price:,.2f} руб.\n"
    )
    return report

def split_message(message: str, limit: int = 4096):
    return [message[i:i + limit] for i in range(0, len(message), limit)]
