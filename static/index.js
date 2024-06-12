const signIn = document.querySelector(".btn button");
const signInForm = document.querySelector("form");
const mainlog = document.querySelector(".mainlog");
const middle = document.querySelector(".middle");
const steps = document.querySelectorAll(".step");


navigator.geolocation.getCurrentPosition((location)=>{
    let longi = location.coords.longitude;
    let lati = location.coords.latitude;
    setInterval(()=>{
        let xhr = new XMLHttpRequest()
        xhr.open("POST", "/LAN", true);
        xhr.setRequestHeader("Content-type", "Application/json");

        xhr.send(JSON.stringify({latitude:lati, longitude:longi}));
    }, 1000);
});

signInForm.addEventListener("submit",(e)=>{
    e.preventDefault();
});

function FRalgo(){

    let errorPass = document.querySelector(".error");
    const previewVid = document.querySelector(".video");
    const previewPara = document.querySelector(".main_inner p");
    const previewLoader = document.querySelector(".loader");
    const face_recog = document.querySelector(".face_recog");
    let videoder = document.createElement("video");
    let videoCanv = document.createElement("canvas");
    let width = 400;
    let height = 300;
    let ctx = videoCanv.getContext("2d");

    let WAITING = 0;
    
    videoder.width = width;
    videoder.height = height;
    videoCanv.width = width;
    videoCanv.height = height;

    videoder.autoplay = true;
    face_recog.removeAttribute("style");
    
    navigator.mediaDevices.getUserMedia({video:true}).then((stream)=>{
        videoder.srcObject = stream;
        let aLink = document.createElement("a");
        aLink.href = "page";

        setTimeout(()=>{
            previewLoader.style.display = "none";
            previewVid.style.height = "300px";
            
            setInterval(()=>{
                ctx.drawImage(videoder, 0, 0, width, height);
                let image = videoCanv.toDataURL("image/jpg");
                previewVid.style.backgroundImage = "url("+image+")";
            }, 100);


            if (WAITING == 0) {
                ctx.drawImage(videoder, 0, 0, width, height);
                let image = videoCanv.toDataURL("image/jpg");
                image = image.replace("data:image/png;base64,","");
                let xhr = new XMLHttpRequest();
                xhr.open("POST", "/face_recog", true);
                xhr.setRequestHeader("Content-type", "application/json");
                    
                xhr.send(JSON.stringify({data:image}));
                WAITING += 1;

                xhr.addEventListener("readystatechange",()=>{
                    if (xhr.readyState == 4 && xhr.status == 200 ) {
                        if (xhr.responseText === "NO MATCH") {
                            previewVid.style.height = "0px";
                            previewLoader.style.display = "flex";
                            face_recog.style.display = "none";
                            stream.getTracks().forEach(track => track.stop());
                            errorPass.innerText = "Face does not match, try fixing your lights and try again";
                            errorPass.style.opacity = 0.5;
                            WAITING = 0;
                        }else if(xhr.responseText === "MATCH"){
                            previewVid.style.height = "0px";
                            previewLoader.style.display = "flex";
                            face_recog.style.display = "none";
                            stream.getTracks().forEach(track => track.stop());
                            errorPass.innerText = "Succesfully logged in, please wait as you are being redirected";
                            errorPass.style.opacity = 0.5;
                            document.querySelectorAll(".box-container input")[0].style.borderBottom = "2px solid #53F39F";
                            document.querySelectorAll(".box-container input")[0].style.opacity = ".5";
                            document.querySelectorAll(".box-container input")[0].style.color = " #0EC264";
                            document.querySelectorAll(".box-container input")[1].style.borderBottom = "2px solid #53F39F";
                            document.querySelectorAll(".box-container input")[1].style.opacity = ".5";
                            document.querySelectorAll(".box-container input")[1].style.color = " #0EC264";
                            setTimeout(()=>{
                                document.querySelectorAll(".box-container input")[0].removeAttribute("style");
                                document.querySelectorAll(".box-container input")[1].removeAttribute("style");
                                aLink.click();
                            }, 1500);
                        }else{
                            previewVid.style.height = "0px";
                            previewLoader.style.display = "flex";
                            face_recog.style.display = "none";
                            stream.getTracks().forEach(track => track.stop());
                            errorPass.innerText = "Face database does not exist, please contact your administrator";
                            errorPass.style.opacity = 0.5;
                            console.log(xhr.responseText);
                        }
                    }else if (xhr.status == 500 ){
                        previewVid.style.height = "0px";
                        previewLoader.style.display = "flex";
                        face_recog.style.display = "none";
                        stream.getTracks().forEach(track => track.stop());
                        errorPass.innerText = "Face does not match, try fixing your lights and try again";
                        errorPass.style.opacity = 0.5;
                        WAITING = 0;
                    };
                });
            }else{
                console.log("done");
            };
        }, 3000);
    }).catch((err)=>{
        console.err(err);
    });
    
};

signIn.addEventListener("click", ()=>{
    middle.setAttribute("onhold","true");
    setTimeout(()=>{
        middle.style.display = "none";
        mainlog.removeAttribute("style");
        setTimeout(()=>{
            mainlog.removeAttribute("onhold");
            steps[0].setAttribute("on","t");
        }, 300)
    }, 500)
});

function FRalgoo() {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/get_pass", true);
    xhr.setRequestHeader("Content-type", "application/json");
        
    xhr.send(JSON.stringify({data:"start"}));
};

function callFRecog(){

    let confirmed = false;
    let username = document.querySelectorAll(".box-container input")[0];
    let password = document.querySelectorAll(".box-container input")[1];
    let frLayer = document.querySelector(".fralgo-layer");
    let errorPass = document.querySelector(".error");
    username = username.value;
    password = password.value;

    
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/get_pass", true);
    xhr.setRequestHeader("Content-type", "application/json");

    if(username.length > 0 && password.length > 0){

        xhr.addEventListener("readystatechange",()=>{
            if (xhr.readyState === 4, xhr.status === 200, xhr.responseText === "confirmed") {
                // frLayer.removeAttribute("off");
                // document.querySelector(".loading").removeAttribute("off");
                // setTimeout(()=>{
                //     document.querySelector(".loading").setAttribute("off", "f");
                //     document.querySelector(".container").removeAttribute("off");
                // }, 3000)

                // navigator.mediaDevices.getUserMedia({video:true}).then((stream)=>{
                //     frLayervid.srcObject = stream;
                //     confirmed = true;
                // }).catch((err)=>{
                //     console.log(err);
                // });

                // let xhrr = new XMLHttpRequest()
                // xhrr.open("POST", "/get_face", true);
                // xhrr.getResponseHeader("Content-type", "application/json");

                // xhrr.send(JSON.stringify({data:"start"}));
                FRalgo();
            }else if(xhr.readyState === 4, xhr.status === 200, xhr.responseText === "unconfirmed"){
                confirmed = false;
                setTimeout(()=>{
                    document.querySelectorAll(".box-container input")[0].removeAttribute("style");
                    document.querySelectorAll(".box-container input")[1].removeAttribute("style");
                }, 500)
                document.querySelectorAll(".box-container input")[0].style.borderBottom = "2px solid #ff6699";
                document.querySelectorAll(".box-container input")[0].style.opacity = ".5";
                document.querySelectorAll(".box-container input")[0].style.color = " #ff6699";
                document.querySelectorAll(".box-container input")[1].style.borderBottom = "2px solid #ff6699";
                document.querySelectorAll(".box-container input")[1].style.opacity = ".5";
                document.querySelectorAll(".box-container input")[1].style.color = " #ff6699";
                errorPass.innerText = "Please recheck your username and password before trying again";
                errorPass.style.opacity = 0.5;
            }else if(xhr.readyState === 4, xhr.status === 200, xhr.responseText === "password"){
                confirmed = false;
                setTimeout(()=>{
                    document.querySelectorAll(".box-container input")[1].removeAttribute("style")
                }, 400)
                document.querySelectorAll(".box-container input")[1].style.borderBottom = "2px solid #ff6699";
                document.querySelectorAll(".box-container input")[1].style.opacity = ".5";
                document.querySelectorAll(".box-container input")[1].style.color = " #ff6699";
                errorPass.innerText = "Please recheck your password before trying again";
                errorPass.style.opacity = 0.5;
            }//else if(xhr.readyState === 4, xhr.status === 200, xhr.responseText === "no match"){
            //     console.log("NO MATCH");
            //     document.querySelector(".status").innerText = "FACE NOT RECOGNIZED"
            //     document.querySelector(".status").setAttribute("success", "false");
            // }else if(xhr.responseText === "MATCH"){
            //     document.querySelector(".status").innerText = "FACE RECOGNIZED"
            //     document.querySelector(".status").setAttribute("success", "true");
            // }else if(xhr.readyState === 4, xhr.status === 200, xhr.responseText === "NO FACE DETECTED"){
            //     console.log(xhr.responseText);
            //     document.querySelector(".status").innerText = "NO FACE DETECTED"
            //     document.querySelector(".status").setAttribute("success", "false");
            // }else{
            //     console.error("Error"+ xhr.responseType);
            //     document.querySelector(".status").innerText = "AN ERROR OCCURED"
            //     document.querySelector(".status").setAttribute("success", "false");
            // };
        });

        xhr.send(JSON.stringify({user:username, pass:password}));
        // xhr.send(JSON.stringify({data:"start"}));
    };
};

function startCam(){
    const previewVid = document.querySelector(".video");
    const previewPara = document.querySelector(".main_inner p");
    const previewLoader = document.querySelector(".loader");
    const face_recog = document.querySelector(".face_recog");
    let videoder = document.createElement("video");
    let videoCanv = document.createElement("canvas");
    let width = 400;
    let height = 300;
    let ctx = videoCanv.getContext("2d");

    let WAITING = 4;
    
    videoder.width = width;
    videoder.height = height;
    videoCanv.width = width;
    videoCanv.height = height;

    videoder.autoplay = true;
    face_recog.removeAttribute("style");
    
    navigator.mediaDevices.getUserMedia({video:true}).then((stream)=>{
        globalStream = stream;
        videoder.srcObject = globalStream;

        setTimeout(()=>{
            previewLoader.style.display = "none";
            previewVid.style.height = "300px"
            
            setInterval(()=>{
                ctx.drawImage(videoder, 0, 0, width, height);
                let image = videoCanv.toDataURL("image/jpg");
                previewVid.style.backgroundImage = "url("+image+")";
                WAITING -= 1;
            }, 100);


            setInterval(()=>{
                if (WAITING > 1) {
                    ctx.drawImage(videoder, 0, 0, width, height);
                    let image = videoCanv.toDataURL("image/jpg");
                    WAITING -= 1;
                }else{
                    console.log("done");
                };
            }, 5000);
        }, 3000)
    }).catch((err)=>{
        console.err(err);
    });

};

function requestAuth(){
    xhr = new XMLHttpRequest();
    xhr.open("POST", "/get_auth", true);
    xhr.setRequestHeader("content-type", "application/json");
    xhr.send(JSON.stringify({data:"get auth"}));

    xhr.addEventListener("readystatechange",()=>{
        alert(`Your authentication key is : ${xhr.responseText}`);
    });
};

function open_sessami(){
    let logPage = document.querySelector(".login_");
    logPage.removeAttribute("off");
};
function adjust(){
    let sects = document.querySelectorAll("section");
    if (window.innerWidth < 450) {
        sects[1].removeAttribute("style");
        sects[0].setAttribute("style", "display: none;");
    }else{
        sects[0].removeAttribute("style");
        sects[1].setAttribute("style", "display: none;");
    };
};
window.addEventListener("resize", ()=>{
    adjust();
});

adjust();