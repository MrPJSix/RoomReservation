import axios from "./api";

const room = {
    getAllRooms(params) {
        return axios.get('studyroom/', {params: params})
    },

    getSeatStatus(params) {
        return axios.get('studyroom/seatstatus/', {params: params})
    }
}
export default room;