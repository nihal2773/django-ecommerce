import { useEffect, useState } from "react";
import API from "../api/axios";

function Cart() {
  const [cart, setCart] = useState([]);

  useEffect(() => {
    API.get("cart/")
      .then((res) => {
        console.log("CART DATA",res.data);
        setCart(res.data);
      })
      .catch((err) => console.log(err));
  }, []);

  return (
    <div>
      <h2>Your Cart</h2>

      {cart.length === 0 ? (
        <p>Cart is empty</p>
      ) : (
        cart.map((item) => (
          <div key={item.id}>
            <h3>{item.product.name}</h3>
            <p>Quantity: {item.quantity}</p>
          </div>
        ))
      )}
    </div>
  );
}

export default Cart;