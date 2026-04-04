import { useEffect, useState } from "react";
import API from "../api/axios";

function Home() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    API.get("products/")
      .then((res) => {
        console.log(res.data);

        if (Array.isArray(res.data)) {
          setProducts(res.data);
        } else if (Array.isArray(res.data.products)) {
          setProducts(res.data.products);
        } else {
          console.error("Invalid data format");
        }
      })
      .catch((err) => console.log(err));
  }, []);

  return (
    <div>
      <h2>Products</h2>

      {products.length === 0 && <p>No products found</p>}

      {products.map((p) => (
        <div key={p.id}>
          <h3>{p.name}</h3>
          <p>{p.price}</p>
        </div>
      ))}
    </div>
  );
}

export default Home;