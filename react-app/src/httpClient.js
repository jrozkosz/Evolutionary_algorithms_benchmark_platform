// author: Jakub Rozkosz

import axios from "axios";

export default axios.create({
  withCredentials: true,
});