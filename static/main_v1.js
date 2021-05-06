/*
Copyright 2017 Google Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
'use strict';

//========== install PWA as mobile app
//let deferredPrompt;
//
//// Listen for the beforeinstallprompt event
//window.addEventListener('beforeinstallprompt', (e) => {
//  // Prevent the mini-infobar from appearing on mobile
//  e.preventDefault();
//  // Stash the event so it can be triggered later.
//  deferredPrompt = e;
//  // Update UI notify the user they can install the PWA
//  showInstallPromotion();
//});
//
//
////// In-app installation flow
////buttonInstall.addEventListener('click', (e) => {
////  // Hide the app provided install promotion
////  hideMyInstallPromotion();
////  // Show the install prompt
////  deferredPrompt.prompt();
////  // Wait for the user to respond to the prompt
////  deferredPrompt.userChoice.then((choiceResult) => {
////    if (choiceResult.outcome === 'accepted') {
////      console.log('User accepted the install prompt');
////      alert('User accepted the install prompt');
////    } else {
////      console.log('User dismissed the install prompt');
////      alert('User dismissed the install prompt');
////    }
////  });
////});
//
//// Detect when the PWA was successfully installed
//window.addEventListener('appinstalled', (evt) => {
//  // Log install to analytics
//  console.log('INSTALL: Success');
//  alert('INSTALL: Success');
//});
//
//// Detect how the PWA was launched
//
//// Track how the PWA was launched
window.addEventListener('DOMContentLoaded', () => {
//  let displayMode = 'browser tab';
//  if (navigator.standalone) {
//    displayMode = 'standalone-ios';
//  }
//  if (window.matchMedia('(display-mode: standalone)').matches) {
//    displayMode = 'standalone';
//  }
//  // Log launch display mode to analytics
//  console.log('DISPLAY_MODE_LAUNCH:', displayMode);
    toggleButton.click();
});
//
//// Track when the display mode changes
//window.addEventListener('DOMContentLoaded', () => {
//  window.matchMedia('(display-mode: standalone)').addListener((evt) => {
//    let displayMode = 'browser tab';
//    if (evt.matches) {
//      displayMode = 'standalone';
//    }
//    // Log display mode change to analytics
//    console.log('DISPLAY_MODE_CHANGED', displayMode);
//  });
//});
var lables = {
    // user labels
    "Excited" : "H/P",
    "Happy" : "H/P",
    "Pleased" : "H/P",
    "Relaxed" : "L/P",
    "Peaceful" : "L/P",
    "Calm" : "L/P",
    "Sleepy" : "L/N",
    "Bored" : "L/N",
    "Sad" : "L/N",
    "Nervous" : "H/N",
    "Annoying" : "H/N",
    "Angry" : "H/N",
    // app labels
    "Anger" : "H/N",
    "Disgust" : "H/N",
    "Fear" : "H/N",
    "Happiness" : "H/P",
    "Neutral" : "L/P",
    "Sadness" : "L/N",
    "Surprise" : "H/P",
};
var user_selection = [];
var app_selection = [];
//========== install PWA as mobile app


var vgaButton = document.querySelector('button#vga');
var qvgaButton = document.querySelector('button#qvga');
var hdButton = document.querySelector('button#hd');
var dimensions = document.querySelector('p#dimensions');
var video = document.querySelector('video');

// screen capture
var screenshotButton = document.querySelector('#screen_buttons');
var popUpImage = document.querySelector('#pop-up-image');
var img = document.querySelector('#screenshot-img');
var showResult = document.querySelector('#show_result');
var image_container = document.querySelector('#image_container');
var toggleButton = document.querySelector('#toggle-btn');
var canvas = document.createElement('canvas');
var pic_count = 0;
var pic_number = image_link.length;
var frame_per_second = 2;
$('input[type="radio"]').click(function(){
    user_selection.push(this.value);
    toggleButton.click();
    $('#screen_buttons').toggle();
});
screenshotButton.onclick = function() {
    if(pic_count>0 && pic_count <= pic_number)
    {
        socket.emit('end_record');
    }
    // clear user selection
    $('input[type="radio"]').each(function () {
		$(this).prop('checked', false);
	})
	if(pic_count !== pic_number)
    {
        recorde_flag = true;
        popUpImage.src = image_link[pic_count];
    }
    //image_number++;
  if(pic_count+1 == pic_number)
    {

        screenshotButton.innerHTML = 'Result';
        toggleButton.click();
        $(this).toggle();
    }
  else
    {
        if(pic_count >= pic_number)
          {
//            alert('No more Picture!!');
            pic_count++;
//            showResult.click();
            var table_body = document.querySelector('#table_body');
//            while(rec_message != pic_number){
//                alert(rec_message,pic_number);
//            }
            if(rec_message != pic_number)
            {
                var myVar2;
                myVar2 = setInterval(function() {
                    if(rec_message == pic_number)
                    {
                        for(var row_num=0;row_num<pic_number;row_num++)
                        {
                            //alert(app_selection[row_num]);
                            var user_l = lables[user_selection[row_num]];
                            var app_l = lables[app_selection[row_num]];

                            var tr_temp = document.createElement('tr');
                            if(user_l == app_l)
                                tr_temp.setAttribute('class', 'table-success');
                            else
                                tr_temp.setAttribute('class', 'table-danger');

                            var td_1 = document.createElement('td');
                            var rw_number = row_num+1;
                            td_1.innerHTML = rw_number.toString();
                            tr_temp.appendChild(td_1);
                            var td_3 = document.createElement('td');
                            td_3.innerHTML = app_l;
                            tr_temp.appendChild(td_3);
                            var td_2 = document.createElement('td');
                            td_2.innerHTML = app_selection[row_num];
                            tr_temp.appendChild(td_2);
                            var td_5 = document.createElement('td');
                            td_5.innerHTML = user_l;
                            tr_temp.appendChild(td_5);
                            var td_4 = document.createElement('td');
                            td_4.innerHTML = user_selection[row_num];
                            tr_temp.appendChild(td_4);
                            table_body.appendChild(tr_temp);
                        }
                        clearInterval(myVar2);
                        location.hash = "#step_2";
                        return;
                    }

                }, 200);
            }

          }
        if(pic_count < pic_number)
            toggleButton.click();
        $(this).toggle();
        screenshotButton.innerHTML = 'Show Next Picture';
    }
  pic_count++;

//  var img_temp = document.createElement('img');
//  canvas.width = video.videoWidth;
//  canvas.height = video.videoHeight;
//  canvas.getContext('2d').drawImage(video, 0, 0);
//  // Other browsers will fall back to image/png
//  img_temp.src = canvas.toDataURL('image/png');
//  img_temp.width = video.videoWidth/10;
//  img_temp.height = video.videoHeight/10;
//  image_container.appendChild(img_temp);
  //document.append()
};
//======
function successCallback(stream) {
  window.stream = stream; // stream available to console
  video.srcObject = stream;
}

function errorCallback(error) {
  console.log('navigator.getUserMedia error: ', error);
  vgaButton.click();
}

//function displayVideoDimensions() {
//  dimensions.textContent = 'Actual video dimensions: ' + video.videoWidth +
//    'x' + video.videoHeight + 'px.';
//}
//var myVar;
//video.addEventListener('play', function() {
//  clearInterval(myVar);
//  //image_container.innerHTML = '';
//  var pic_counter = 0;
//  myVar = setInterval(function() {
////    displayVideoDimensions();
//    if(pic_counter < 10)
//    {
//        //screenshotButton.click();
//        pic_counter++;
//    }
//    else
//    {
//        clearInterval(myVar);
//        pic_counter = 0;
//    }
//  }, 1000);
//});

var qvgaConstraints = {
    audio: false,
      video: {
        width: { max: 320 },
        height: { max: 240 }
      }
}

var vgaConstraints = {
  audio: false,
      video: {
        width: { max: 640 },
        height: { max: 480 }
      }
};

var hdConstraints = {
  audio: false,
      video: {
        width: { max: 1280 },
        height: { max: 720 }
      }
};

qvgaButton.onclick = function() {
  getMedia(qvgaConstraints);
};
vgaButton.onclick = function() {
  getMedia(vgaConstraints);
};
hdButton.onclick = function() {
  getMedia(hdConstraints);
};

function getMedia(constraints) {
  if (window.stream) {
    video.src = null;
    window.stream.getVideoTracks()[0].stop();
  }
  navigator.mediaDevices.getUserMedia(
    constraints
  ).then(
    successCallback,
    errorCallback
  );
}

if ('serviceWorker' in navigator) {
    navigator.serviceWorker
    .register('./service-worker.js')
    .then(function(registration) {
        console.log('Service Worker Registered!');
        return registration;
    })
    .catch(function(err) {
        console.error('Unable to register service worker.', err);
    });
}

//hdButton.click();
qvgaButton.click();

//================== send image to server
function findGetParameter(parameterName) {
    var result = null,
        tmp = [];
    window.location.search
        .substr(1)
        .split("&")
        .forEach(function (item) {
          tmp = item.split("=");
          if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
        });
    return result;
}
var url_param = findGetParameter('new_url');
var recorde_flag = false;
//    var socket = io('http://127.0.0.1:8080');
//    var socket = io('http://vibe:80');
    var socket = io();

var tta = '';
//var socket = io('https://vibe-ml-engine-o5tympfaqq-lz.a.run.app/:8080');
socket.on('connect', function(){
  console.log('connected');
});
//socket.on('client event', function(data){console.log('my event');});
socket.on('disconnect', function(){console.log('disconnect');});

function sendmessage() {
    var img_temp = document.createElement('img');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    var new_message = canvas.toDataURL('image/png');
    //alert (new_message);
    img_temp.src = canvas.toDataURL('image/png');
    img_temp.width = video.videoWidth/10;
    img_temp.height = video.videoHeight/10;
    image_container.appendChild(img_temp);
    socket.emit('start_record', new_message);

}
var rec_message = 0;
socket.on('new_message_client_temp', function (data) {
    if(data.error == 'None')
  {
    var data_temp = data.response
    var arousal = 0
    var valence = 0
    for (var prop in data_temp) {
      if (data_temp.hasOwnProperty(prop)) {
        if(prop == 'arousal')
            arousal = parseFloat(data_temp[prop])
        else if(prop == 'valence')
            valence = parseFloat(data_temp[prop])
      }
    }
//    alert(rec_message);
//    alert(app_selection);
    console.log(arousal);
    console.log(valence);
    console.log(data.response);
  }
  else
//    alert(data.error);
    {
        console.log(data.error);
        console.log(data.response);
        console.log(data);
    }
});

socket.on('new_message_client', function (data) {
//    alert('test')
  //socket.broadcast.emit('new_message', data);
  if(data.error == 'None')
  {
    var data_temp = data.response
    var maxProp = null
    var maxValue = -1
    for (var prop in data_temp) {
      if (data_temp.hasOwnProperty(prop)) {
        var value = parseFloat(data_temp[prop])
        if (value > maxValue) {
          maxProp = prop
          maxValue = value
        }
      }
    }
    app_selection.push(maxProp);
    rec_message++;
//    alert(rec_message);
//    alert(app_selection);
    console.log(maxProp);
    console.log(maxValue);
    console.log(data.response);
    console.log(app_selection);
  }
  else
    alert(data.error);
});
var myVar;
myVar = setInterval(function() {
    if(recorde_flag === true)
        sendmessage();
}, 1000/frame_per_second);
//================== wheel selector

var nbOptions = 7;
var angleStart = -360;

// jquery rotate animation
function rotate(li,d) {
    $({d:angleStart}).animate({d:d}, {
        step: function(now) {
            now+=30;
            $(li)
               .css({ transform: 'rotate('+now+'deg)' })
               .find('label')
                  .css({ transform: 'rotate('+(-now)+'deg)' });
        }, duration: 0
    });
}

// show / hide the options
function toggleOptions(s) {
    $(s).toggleClass('open');
    var li = $(s).find('li');
    var deg = $(s).hasClass('half') ? 180/(li.length-1) : 360/li.length;
    for(var i=0; i<li.length; i++) {
        var d = $(s).hasClass('half') ? (i*deg)-90 : i*deg;
        $(s).hasClass('open') ? rotate(li[i],d) : rotate(li[i],angleStart);
    }
}

$('.selector button').click(function(e) {
    toggleOptions($(this).parent());
});

setTimeout(function() { toggleOptions('.selector'); }, 100);//@ sourceURL=pen.js

//================== wheel selector

//================== bar chart
// REf
// http://stackoverflow.com/questions/40061862/chart-js-update-bars-of-a-bar-chart

var canvas = document.getElementById("barChart");
var ctx = canvas.getContext('2d');
var chartType = 'bar';
var myBarChart;

// Global Options:
Chart.defaults.global.defaultFontColor = 'grey';
Chart.defaults.global.defaultFontSize = 16;

var data = {
  labels: ["Neutral", "Anger", "Disgust", "Fear", "Happiness", "Sadness", "Surprise"],
  datasets: [{
    label: "Facial Emotion Recognition",
    fill: true,
    lineTension: 0.1,
    backgroundColor: "rgba(0,255,0,0.4)",
    borderColor: "green", // The main line color
    borderCapStyle: 'square',
    pointBorderColor: "white",
    pointBackgroundColor: "green",
    pointBorderWidth: 1,
    pointHoverRadius: 8,
    pointHoverBackgroundColor: "yellow",
    pointHoverBorderColor: "green",
    pointHoverBorderWidth: 2,
    pointRadius: 4,
    pointHitRadius: 10,
    data: [0.3, 0.8, 0.1, 0.0, 0.1, 0.1, 0.4],
    spanGaps: true,
  }]
};

var options = {
  scales: {
    yAxes: [{
      ticks: {
        beginAtZero: true
      }
    }]
  },
  title: {
    fontSize: 18,
    display: true,
    text: 'Percentage of Emotions',
    position: 'bottom'
  }
};

init();

function init() {
  // Chart declaration:
  myBarChart = new Chart(ctx, {
    type: chartType,
    data: data,
    options: options
  });
}

function addData() {
  myBarChart.data.labels[12] ="2017";
  myBarChart.data.labels[13] ="2018";
  myBarChart.data.datasets[0].data[12] = 500;
  myBarChart.data.datasets[0].data[13] = 600;
  myBarChart.update();
}

function adjust2016() {
  myBarChart.data.datasets[0].data[11] = 300;
  myBarChart.update();
}