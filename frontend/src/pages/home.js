import { useEffect, useState } from "react";
import API from "../api/axios";

function Cart() {
  const [cart, setCart] = useState([]);

  // 🔹 FETCH CART
  useEffect(() => {
    API.get("cart/")
      .then((res) => {
        console.log("CART DATA:", res.data);

        // handle different backend formats
        if (Array.isArray(res.data)) {
          setCart(res.data);
        } else if (Array.isArray(res.data.cart)) {
          setCart(res.data.cart);
        } else if (Array.isArray(res.data.items)) {
          setCart(res.data.items);
        } else {
          console.log("Unexpected format");
          setCart([]);
        }
      })
      .catch((err) => {
        console.log("CART ERROR:", err.response);
      });
  }, []);

  // 🔹 REMOVE FROM CART
  const removeFromCart = (id) => {
    API.delete(`cart/remove/${id}/`)
      .then((res) => {
        console.log("REMOVED:", res.data);

        // update UI instantly
        setCart((prev) => prev.filter((item) => item.id !== id));
      })
      .catch((err) => {
        console.log("REMOVE ERROR:", err.response);
        alert("Error removing item");
      });
  };

  return (
    <div>
      <h2>Your Cart</h2>

      {/* 🔹 EMPTY STATE */}
      {cart.length === 0 ? (
        <p>Cart is empty</p>
      ) : (
        cart.map((item) => (
          <div key={item.id}>
            <h3>
              {item.product?.name || "No product name"}
            </h3>

            <p>Quantity: {item.quantity}</p>

            <button onClick={() => removeFromCart(item.id)}>
              Remove
            </button>

            <hr />
          </div>
        ))
      )}
    </div>
  );
}

export default Cart;