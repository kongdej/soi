
const APPID = "PudzaSOI";
const KEY = "24EAjwakpnDLCRw";
const SECRET = "IlRbpgpXChT2iNJAWkCvqmiwJ";
const ALIAS = "web";

var microgear = Microgear.create({
    key: KEY,
    secret: SECRET,
    alias : ALIAS
});

microgear.on('message',function(topic,msg) {
    printMsg(topic,msg);
    if (topic == "/PudzaSOI/gearname/web") {
        
        var relays = msg.split(',');
       if (relays[0] ==  '1')
            $('#pump_btn').prop('checked', true).change();
        else
            $('#pump_btn').prop('checked', false).change();
       if (relays[1] ==  '1')
            $('#light_btn').prop('checked', true).change();
        else
            $('#light_btn').prop('checked', false).change();
       if (relays[2] ==  '1')
            $('#co2_btn').prop('checked', true).change();
        else
            $('#co2_btn').prop('checked', false).change();
 
    }

    if (topic == "/PudzaSOI/data") {
        var datas = msg.split(',');
        g_wtrtemp.refresh(datas[0]);
        g_ec.refresh(datas[1]);
        g_tub.refresh(datas[2]);
        g_PH.refresh(datas[3]);
    }
    else if (topic == "/PudzaSOI/eccalmsg") {
        $('#echo_eccal').text(msg);
    }

});

microgear.on('connected', function() {
    printMsg('Init',"Connected to NETPIE...");
    microgear.setAlias(ALIAS);
    microgear.subscribe("/data");
    microgear.subscribe("/cmd");
    microgear.subscribe("/eccalmsg");
});

microgear.on('present', function(event) {
    printMsg(event.alias,event.type);
});

microgear.on('absent', function(event) {
    printMsg(event.alias,event.type);
});

microgear.resettoken(function(err) {
    microgear.connect(APPID);
});


$("#cb").click(function () {
    console.log($('#ec_cal').val());
    microgear.publish ("/cmd", '1'+$('#ec_cal').val());
});



$("#pump_btn").change(function () {
//    console.log($(this).prop('checked'));
    if ($(this).prop('checked'))
        microgear.chat ("uno", "01");
    else 
        microgear.chat ("uno", "00");
});


$("#light_btn").change(function () {
//    console.log($(this).prop('checked'));
    if ($(this).prop('checked'))
        microgear.chat ("uno", "11");
    else 
        microgear.chat ("uno", "10");
});

$("#co2_btn").change(function () {
//    console.log($(this).prop('checked'));
    if ($(this).prop('checked'))
        microgear.chat ("uno", "21");
    else 
        microgear.chat ("uno", "20");
});

$("#mode_btn").change(function () {
    if ($(this).prop('checked')) {
        $('#pump_btn').bootstrapToggle('disable');
        $('#light_btn').bootstrapToggle('disable');
        $('#co2_btn').bootstrapToggle('disable');
    }
    else {
        $('#pump_btn').bootstrapToggle('enable');
        $('#light_btn').bootstrapToggle('enable');
        $('#co2_btn').bootstrapToggle('enable');
    } 
});

function printMsg(topic,msg) {
    var now = new Date();
    var d = now.getDay();
    var m = now.getMonth();
    m += 1;  
    var y = now.getFullYear();
    var h = now.getHours();
    var i = now.getMinutes();
    var s = now.getSeconds();
    var datetime = d + "/" + m + "/" + y + " " + h + ":" + i + ":" + s;
   document.getElementById("data").innerHTML = '&nbsp;<i class="fa fa-bell-o"></i> '+ datetime + ' # ' +topic+' <i class="fa fa-ellipsis-h"></i> ' + msg;
}

var g_wtrtemp = new JustGage({
    id: "gaugeWtrTemp",
    value: 0,
    value:0,
    min: 0,
    max: 50,
    decimals:1,
    relativeGaugeSize: true,
    counter: true,
    formatNumber:true,
    gaugeWidthScale: 1,
    title: "Temperature",
    label:"C",
    titlePosition: "below",
    titleFontSize: "5px",
    titleFontFamily: "Arial"
  });

var g_ec = new JustGage({
    id: "gaugeEC",
    value: 0,
    value:0,
    min: 0,
    max: 5,
    relativeGaugeSize: true,
    gaugeWidthScale: 1,
    decimals:2,
    title: "EC",
    label:"mS/cm",
    titlePosition: "below",
    titleFontSize: "5px",
    titleFontFamily: "Arial"
  });

var g_tub = new JustGage({
    id: "gaugeTub",
    value: 0,
    value:0,
    min: 0,
    max: 4000,
    decimals:2,
    relativeGaugeSize: true,
    decimals:true,
    gaugeWidthScale: 1,
    title: "Turbidity",
    label:"mg/L",
    titlePosition: "below"
  });

var g_PH = new JustGage({
    id: "gaugePH",
    value: 0,
    value:0,
    min: 1,
    max: 14,
    decimals:2,
    relativeGaugeSize: true,
    gaugeWidthScale: 1,
    title: "PH",
    label:"",
    titlePosition: "below"
  });
