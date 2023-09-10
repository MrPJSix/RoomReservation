import axios from "./api";
// import base from "./base";

const campus = {
    getAllCampus() {
        return axios.get("/campus/")
    },

    getBuildingsByCampus(params) {
        console.log(params)
        return axios.get("/building/", {params: params})
    }
}
export default campus;