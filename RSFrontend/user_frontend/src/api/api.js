import axios from "axios";
// import base from "./base";

const instance = axios.create({
    baseURL: "/api",
    timeout: 50000,
    // withCredentials: false
})

async function getCsrfToken() {
  try {
      const response = await axios.get('/api/csrf-token/');
      console.log(response.data.csrfToken)
      console.log(response.headers)
      sessionStorage.setItem("csrf_token", response.data.csrfToken)
      console.log("~~~~~~~~",document.cookie)
      let cookie = document.cookie  //提取cookie
      let csrf_token = cookie.split("=")[1]  //提取cookie中的csrftoken
      console.log("csrf:  ", csrf_token)
      return response.data.csrfToken;
    //   return csrf_token;
  } catch (error) {
      console.error('Error fetching CSRF token:', error);
      return null;
  }
}

instance.defaults.withCredentials = true;

instance.defaults.headers.post["Content-Type"] = 
  "application/x-www-form-urlencoded; charset=UTF-8";


(async () => {
    const csrfToken = await getCsrfToken();
    if (csrfToken) {
        instance.defaults.headers.common['X-CSRFToken'] = csrfToken;
        // instance.defaults.headers.common['X-Csrftoken'] = csrfToken;
    } else {
        console.error('Unable to set CSRF token for Axios requests.');
    }
})();


// /**
//  * 请求拦截器
//  */
// instance.interceptors.request.use(
//     (config) => {
//         config.headers['X-CSRFToken'] = cookie.parse(document.cookie).csrftoken;
//         return config
//     },
//     (error) => Promise.error(error)
// )

// /**
//  * 响应拦截器
//  */
// instance.interceptors.response.use(
//     res => {
//       console.log(res.data)
//         return res.data
//     }, err => {
//         return Promise.reject(err)
//     }
// )

export default instance