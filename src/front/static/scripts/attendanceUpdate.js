function getAttendanceList() {
    let attendanceList = document.querySelector('#lista-presentes');
    let listItems = attendanceList.querySelectorAll('li');
    let students = [];
    for (let li of listItems){
        students.push(li.textContent);
    }

    return students;
}

const attendanceUpdate = (socket ) => {

    socket.on("update_list", (data)=> {
        newlyDetected = [];
        currentStudents = getAttendanceList();

        for (let student of data.faces) {
            if (currentStudents.indexOf(student) == -1) {
                newlyDetected.push(student);
            }
        }
        let attendanceList = document.querySelector('#lista-presentes');
        for (let face of newlyDetected) {
            let student = document.createElement("li");
            student.innerText = face;
            student.classList.add("text-light");
            attendanceList.appendChild(student);
        }
    });   
}

attendanceUpdate();

