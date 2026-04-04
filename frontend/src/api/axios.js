import axios from "axios";

const API = axios.create({
  baseURL: "https://django-backend-2bnc.onrender.com/api/",
});

export default API;