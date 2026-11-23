/*
   Licensed to the Apache Software Foundation (ASF) under one or more
   contributor license agreements.  See the NOTICE file distributed with
   this work for additional information regarding copyright ownership.
   The ASF licenses this file to You under the Apache License, Version 2.0
   (the "License"); you may not use this file except in compliance with
   the License.  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/
var showControllersOnly = false;
var seriesFilter = "";
var filtersOnlySampleSeries = true;

/*
 * Add header in statistics table to group metrics by category
 * format
 *
 */
function summaryTableHeader(header) {
    var newRow = header.insertRow(-1);
    newRow.className = "tablesorter-no-sort";
    var cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Requests";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 3;
    cell.innerHTML = "Executions";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 7;
    cell.innerHTML = "Response Times (ms)";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Throughput";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 2;
    cell.innerHTML = "Network (KB/sec)";
    newRow.appendChild(cell);
}

/*
 * Populates the table identified by id parameter with the specified data and
 * format
 *
 */
function createTable(table, info, formatter, defaultSorts, seriesIndex, headerCreator) {
    var tableRef = table[0];

    // Create header and populate it with data.titles array
    var header = tableRef.createTHead();

    // Call callback is available
    if(headerCreator) {
        headerCreator(header);
    }

    var newRow = header.insertRow(-1);
    for (var index = 0; index < info.titles.length; index++) {
        var cell = document.createElement('th');
        cell.innerHTML = info.titles[index];
        newRow.appendChild(cell);
    }

    var tBody;

    // Create overall body if defined
    if(info.overall){
        tBody = document.createElement('tbody');
        tBody.className = "tablesorter-no-sort";
        tableRef.appendChild(tBody);
        var newRow = tBody.insertRow(-1);
        var data = info.overall.data;
        for(var index=0;index < data.length; index++){
            var cell = newRow.insertCell(-1);
            cell.innerHTML = formatter ? formatter(index, data[index]): data[index];
        }
    }

    // Create regular body
    tBody = document.createElement('tbody');
    tableRef.appendChild(tBody);

    var regexp;
    if(seriesFilter) {
        regexp = new RegExp(seriesFilter, 'i');
    }
    // Populate body with data.items array
    for(var index=0; index < info.items.length; index++){
        var item = info.items[index];
        if((!regexp || filtersOnlySampleSeries && !info.supportsControllersDiscrimination || regexp.test(item.data[seriesIndex]))
                &&
                (!showControllersOnly || !info.supportsControllersDiscrimination || item.isController)){
            if(item.data.length > 0) {
                var newRow = tBody.insertRow(-1);
                for(var col=0; col < item.data.length; col++){
                    var cell = newRow.insertCell(-1);
                    cell.innerHTML = formatter ? formatter(col, item.data[col]) : item.data[col];
                }
            }
        }
    }

    // Add support of columns sort
    table.tablesorter({sortList : defaultSorts});
}

$(document).ready(function() {

    // Customize table sorter default options
    $.extend( $.tablesorter.defaults, {
        theme: 'blue',
        cssInfoBlock: "tablesorter-no-sort",
        widthFixed: true,
        widgets: ['zebra']
    });

    var data = {"OkPercent": 82.88987435328899, "KoPercent": 17.110125646711012};
    var dataset = [
        {
            "label" : "FAIL",
            "data" : data.KoPercent,
            "color" : "#FF6347"
        },
        {
            "label" : "PASS",
            "data" : data.OkPercent,
            "color" : "#9ACD32"
        }];
    $.plot($("#flot-requests-summary"), dataset, {
        series : {
            pie : {
                show : true,
                radius : 1,
                label : {
                    show : true,
                    radius : 3 / 4,
                    formatter : function(label, series) {
                        return '<div style="font-size:8pt;text-align:center;padding:2px;color:white;">'
                            + label
                            + '<br/>'
                            + Math.round10(series.percent, -2)
                            + '%</div>';
                    },
                    background : {
                        opacity : 0.5,
                        color : '#000'
                    }
                }
            }
        },
        legend : {
            show : true
        }
    });

    // Creates APDEX table
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [0.8288987435328898, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [1.0, 500, 1500, "Clientes · buscar ciudad"], "isController": false}, {"data": [0.074, 500, 1500, "Clientes · rastrear envío"], "isController": false}, {"data": [1.0, 500, 1500, "Preparación · registrar envío"], "isController": false}, {"data": [1.0, 500, 1500, "Operadores · registrar envío"], "isController": false}, {"data": [1.0, 500, 1500, "Clientes · sugerencias del chatbot"], "isController": false}, {"data": [1.0, 500, 1500, "Preparación · ingreso operador"], "isController": false}, {"data": [1.0, 500, 1500, "Operadores · reimprimir comprobante"], "isController": false}, {"data": [1.0, 500, 1500, "Operadores · iniciar sesión"], "isController": false}, {"data": [1.0, 500, 1500, "Clientes · historial del envío"], "isController": false}, {"data": [1.0, 500, 1500, "Clientes · horario de recogidas"], "isController": false}]}, function(index, item){
        switch(index){
            case 0:
                item = item.toFixed(3);
                break;
            case 1:
            case 2:
                item = formatDuration(item);
                break;
        }
        return item;
    }, [[0, 0]], 3);

    // Create statistics table
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 5412, 926, 17.110125646711012, 31.106984478935757, 1, 293, 23.0, 64.0, 86.34999999999945, 143.0, 76.53147802477515, 43.9294866525963, 36.78527655958341], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["Clientes · buscar ciudad", 1000, 0, 0.0, 41.83399999999999, 9, 272, 33.0, 75.0, 100.0, 167.91000000000008, 15.508684863523573, 7.360567230148883, 7.330276830024814], "isController": false}, {"data": ["Clientes · rastrear envío", 1000, 926, 92.6, 11.694000000000008, 1, 145, 7.0, 26.0, 40.0, 70.99000000000001, 15.533980582524272, 6.635618932038835, 7.25121359223301], "isController": false}, {"data": ["Preparación · registrar envío", 1, 0, 0.0, 58.0, 58, 58, 58.0, 58.0, 58.0, 58.0, 17.241379310344826, 14.412715517241379, 13.621363146551724], "isController": false}, {"data": ["Operadores · registrar envío", 200, 0, 0.0, 61.294999999999966, 16, 209, 53.0, 111.80000000000001, 123.84999999999997, 168.91000000000008, 4.122606311710263, 3.44612043421351, 3.2794044895182735], "isController": false}, {"data": ["Clientes · sugerencias del chatbot", 1000, 0, 0.0, 23.322999999999976, 4, 168, 18.0, 43.0, 56.94999999999993, 100.99000000000001, 15.56783684906982, 13.333000895150619, 7.206205728963961], "isController": false}, {"data": ["Preparación · ingreso operador", 1, 0, 0.0, 161.0, 161, 161, 161.0, 161.0, 161.0, 161.0, 6.211180124223602, 4.634122670807454, 1.4436141304347825], "isController": false}, {"data": ["Operadores · reimprimir comprobante", 200, 0, 0.0, 46.589999999999996, 12, 293, 39.0, 79.80000000000001, 105.79999999999995, 202.71000000000026, 4.111250436820359, 2.2122060455937675, 1.955252893292495], "isController": false}, {"data": ["Operadores · iniciar sesión", 10, 0, 0.0, 164.2, 94, 285, 168.0, 277.20000000000005, 285.0, 285.0, 0.5490282200505106, 0.4096265235533107, 0.12760616833205227], "isController": false}, {"data": ["Clientes · historial del envío", 1000, 0, 0.0, 43.47199999999995, 10, 245, 34.0, 84.0, 102.0, 153.95000000000005, 15.562749003984063, 7.735780510769422, 7.386226578062749], "isController": false}, {"data": ["Clientes · horario de recogidas", 1000, 0, 0.0, 24.58999999999998, 5, 236, 18.0, 47.0, 65.0, 118.0, 15.580935167728768, 8.840354816846107, 7.273131845873389], "isController": false}]}, function(index, item){
        switch(index){
            // Errors pct
            case 3:
                item = item.toFixed(2) + '%';
                break;
            // Mean
            case 4:
            // Mean
            case 7:
            // Median
            case 8:
            // Percentile 1
            case 9:
            // Percentile 2
            case 10:
            // Percentile 3
            case 11:
            // Throughput
            case 12:
            // Kbytes/s
            case 13:
            // Sent Kbytes/s
                item = item.toFixed(2);
                break;
        }
        return item;
    }, [[0, 0]], 0, summaryTableHeader);

    // Create error table
    createTable($("#errorsTable"), {"supportsControllersDiscrimination": false, "titles": ["Type of error", "Number of errors", "% in errors", "% in all samples"], "items": [{"data": ["429", 926, 100.0, 17.110125646711012], "isController": false}]}, function(index, item){
        switch(index){
            case 2:
            case 3:
                item = item.toFixed(2) + '%';
                break;
        }
        return item;
    }, [[1, 1]]);

        // Create top5 errors by sampler
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 5412, 926, "429", 926, "", "", "", "", "", "", "", ""], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": [], "isController": false}, {"data": ["Clientes · rastrear envío", 1000, 926, "429", 926, "", "", "", "", "", "", "", ""], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
