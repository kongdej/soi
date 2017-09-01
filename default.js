
    function customValue(val) {
        return val;        
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
        relativeGaugeSize: true,
        gaugeWidthScale: 1,
        title: "PH",
        label:"",
        titlePosition: "below"
      });

    const APPID = "PudzaSOI";
    const KEY = "24EAjwakpnDLCRw";
    const SECRET = "IlRbpgpXChT2iNJAWkCvqmiwJ";

    const ALIAS = "web";

    var microgear = Microgear.create({
        key: KEY,
        secret: SECRET,
        alias : ALIAS
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


    microgear.on('message',function(topic,msg) {
        printMsg(topic,msg);

        if (topic.indexOf('web') != -1) {
            $("#s_nodemcu").removeClass("btn-default");
            $("#s_nodemcu").addClass("btn-warning");
        }
        if (topic.indexOf('uno') != -1) {
            $("#s_arduino").removeClass("btn-default");
            $("#s_arduino").addClass("btn-warning");
        }

        if (topic == "/PudzaSOI/temp") {
            g_wtrtemp.refresh(msg);
        }
        else if (topic == "/PudzaSOI/ec") {
            g_ec.refresh(msg);
        }
        else if (topic == "/PudzaSOI/tub") {
            g_tub.refresh(msg);
        }
        else if (topic == "/PudzaSOI/ph") {
            g_PH.refresh(msg);
        }

        else if (topic == "/PUDZAHydro/nodemcu") {
            var vals = msg.split(",");
            g_light.refresh(vals[0]);
            g_gtemp.refresh(vals[1]);
            if (vals[2] == '1') {
                $('#mist_status').text('ON');
            }
            else {
                $('#mist_status').text('OFF');
            }
        }
        else if (topic == "/PudzaSOI/eccalmsg") {
            $('#echo_eccal').text(msg);
        }
        else {
//            document.getElementById("data").innerHTML = now.getDay() + ":[" + topic+ "] " + msg;
        }
    });

    microgear.on('connected', function() {
        printMsg('Init',"Connected to NETPIE...");
        $("#s_htmlgear").removeClass("btn-default");
        $("#s_htmlgear").addClass("btn-warning");
        microgear.setAlias(ALIAS);
        microgear.subscribe("/temp")        
        microgear.subscribe("/ec");
        microgear.subscribe("/tub");
        microgear.subscribe("/ph");
        microgear.subscribe("/cmd");
        microgear.subscribe("/eccalmsg");
    });

    microgear.on('present', function(event) {
        printMsg(event.alias,event.type);
        if (event.alias == "reporter") {
            if (event.type == "aliased") {
                $("#s_reporter").removeClass("btn-default");
                $("#s_reporter").addClass("btn-warning");
            }
        }
        console.log(event);
    });

    microgear.on('absent', function(event) {
        printMsg(event.alias,event.type);
        if (event.alias == "reporter") {
            if (event.type == "offline") {
                $("#s_reporter").removeClass("btn-warning");
                $("#s_reporter").addClass("btn-default");
            }
        }
        if (event.alias == "raspiPython") {
            if (event.type == "offline") {
                $("#s_arduino").removeClass("btn-warning");
                $("#s_arduino").addClass("btn-default");
            }
        }
        if (event.alias == "nodemcu") {
            if (event.type == "offline") {
                $("#s_nodemcu").removeClass("btn-warning");
                $("#s_nodemcu").addClass("btn-default");
            }
        }

        console.log(event);
    });

    microgear.resettoken(function(err) {
        microgear.connect(APPID);
    });

    $("#cb").click(function () {
        console.log($('#ec_cal').val());
        microgear.publish ("/cmd", '1'+$('#ec_cal').val());
    });

    $("#csp_temp").click(function () {
        console.log($('#sp_temp').val());
        microgear.publish ("/sptemp", $('#sp_temp').val());
    });

    $("#miston").click(function () {
        console.log("on");
        microgear.publish ("/mist", "1");
    });

    $("#mistoff").click(function () {
        console.log("off");
        microgear.publish ("/mist", "0");
    });
