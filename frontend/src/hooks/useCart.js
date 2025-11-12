import { useState } from 'react'

export default function useCart() {
  const [items, setItems] = useState([]) // {menu_item_id, name, price_cents, quantity}
}
