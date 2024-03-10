function include(file) { 
  
    var script  = document.createElement('script'); 
    script.src  = file; 
    script.type = 'text/javascript'; 
    script.defer = true; 
    
    document.getElementsByTagName('head').item(0).appendChild(script); 
    
}

// sheetJS
include("/static/node_modules/xlsx/dist/xlsx.full.min.js")
// import XLSX from '../../../personal_matters/static/node_modules/xlsx/xlsx'

// bootstrap-table
include("/static/node_modules/bootstrap-table/dist/bootstrap-table.min.js")


// import jquery from "../../../personal_matters/static/node_modules/jquery/dist/jquery.js"

var global_csv = null;
var global_multipate_add_ajax_num = 0;
var csv_encoding = 'utf-8';
var ajaxQueue = $({});


window.onload=function(){
    let ignore_column = ["csrfmiddlewaretoken", "go_live_at", "expire_at"]
    let select_field = ["receipt_disbursement", "transaction_category", "transaction_status"]
    let int_field = ["amount"]
    let date_time_field = ["transaction_time"]

    // csv load event
    document.getElementById('csvFileInput').addEventListener('change', async function() {
        var file = this.files[0];
        var reader = new FileReader();
    
        reader.onload = function(e) {
            let csvContent = e.target.result;
            const wb = XLSX.read(csvContent, {type: 'string'});
            const ws = wb.Sheets[wb.SheetNames[0]];
            global_csv = ws;
            // csv_load_table_init
            let ledger_form = document.getElementById("id_create_ledger_form")
            let ledger_form_data = new FormData(ledger_form)
            let form_column = []
            let form_fields = []
            for (var pair of ledger_form_data.entries()) {
                if (ignore_column.indexOf(pair[0]) >= 0) {
                    continue;
                }
                form_fields.push(pair[0])
                form_column.push({
                    field: pair[0],
                    title: pair[0],
                    align: 'center',
                    // formatter: strFormatter,
                })
            }
            $('#csv_load_table').bootstrapTable('destroy').bootstrapTable({
                columns:[form_column],
                showFullscreen: true,
                height: 500,
            })
            let data = XLSX.utils.sheet_to_json(ws, { raw: false });
            if (document.getElementById("check_each_entry").checked) {
                data.forEach(json_data => {
                    result_status = fields_check(json_data, form_fields)
                    if (!result_status) {
                        alert("field not found: "+form_fields+";\n entry:"+json_data)
                        return -1
                    }
                });   

            }

            for (const i in data) {
                if (Object.hasOwnProperty.call(data, i)) {
                    const json_data = data[i];
                    for (const j in int_field) {
                        if (Object.hasOwnProperty.call(int_field, j)) {
                            const element = int_field[j];
                            data[i][element] = parseInt(Number(data[i][element]) * 100)
                        }
                    }
                    for (const j in select_field) {
                        if (Object.hasOwnProperty.call(select_field, j)) {
                            const element = select_field[j];
                            // console.log(data[i][element])
                            data[i][element] = get_select_value_option_text("id_"+element, data[i][element])
                        }
                    }
                    for (const j in date_time_field) {
                        if (Object.hasOwnProperty.call(date_time_field, j)) {
                            const date_time = date_time_field[j];
                            data[i][date_time] = formatTime(data[i][date_time]);
                        }
                    }
                }
            }
            $('#csv_load_table').bootstrapTable('append', data)
        };
    
        reader.readAsText(file, csv_encoding);

    });

    // csv encoding input event
    document.getElementById('file_encoding').addEventListener('change', function () {
        csv_encoding = this.value;
    });
    document.getElementById('id_csv_template_button').addEventListener('click', function () {
        let ledger_form = document.getElementById("id_create_ledger_form")
        let ledger_form_data = new FormData(ledger_form)
        let form_column = []
        let ignore_column = ["csrfmiddlewaretoken", "go_live_at", "expire_at"]
        for (var pair of ledger_form_data.entries()) {
            if (ignore_column.indexOf(pair[0]) >= 0) {
                continue;
            }
            form_column.push(pair[0])
          }
        const ws = XLSX.utils.aoa_to_sheet([form_column]);
        const csv = XLSX.utils.sheet_to_csv(ws);
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        document.body.appendChild(a);
        a.href = url;
        a.download = 'template.csv';
        a.click();
        window.URL.revokeObjectURL(url);
    })


    //confirm_button
    document.getElementById("id_multipate_ledger_confirm_button").addEventListener("click", function () {
        const data = $('#csv_load_table').bootstrapTable("getData",{useCurrentPage:false,includeHiddenRows:true})
        var ajaxQueue = $({});
        data.forEach(entry => {
            const ignore_column = ["go_live_at", "expire_at"]
            // const XHR = new XMLHttpRequest();
            // XHR.addEventListener("load", (event) => {
            //     console.log("send succeed");
            //   });
            // XHR.addEventListener("error", (event) => {
            //     console.log(event);
            // });
            const ledger_form = document.getElementById("id_create_ledger_form")
            // const tocken = ledger_form.
            const ledger_form_data = new FormData(ledger_form)
            for (const i in ignore_column) {
                if (Object.hasOwnProperty.call(ignore_column, i)) {
                    const ignore_field = ignore_column[i];
                    ledger_form_data.delete(ignore_field)
                }
            }

            for (const key in entry) {
                if (Object.hasOwnProperty.call(entry, key)) {
                    const element = entry[key];
                    ledger_form_data.set(key, element)
                }
            }

            ledger_form_data.append("action-publish", "action-publish")
            const formDataEntries = Array.from(ledger_form_data.entries());

            // 将 FormData 数据转换为对象形式
            const formDataObject = formDataEntries.reduce((acc, [key, value]) => {
                                        acc[key] = value;
                                        return acc;
                                    }, {});
            const data_submit = Object.keys(formDataObject).map(key => encodeURIComponent(key) + '=' + encodeURIComponent(formDataObject[key])).join('&');
            // console.log(data_submit)
            // XHR.open(ledger_form.method, ledger_form.action);
            // XHR.send(data)

            // $.ajax({
            //     type:ledger_form.method,
            //     url:ledger_form.action,
            //     data: data_submit,
            //     dataType: 'application/x-www-form-urlencoded',
            //     beforeSend: function(xhr) {
            //         global_multipate_add_ajax_num += 1;
            //       },
            //     success: function(response) {
            //         console.log(response);
            //         global_multipate_add_ajax_num -= 1;
            //       },
            // })
            queueAjaxRequest(ledger_form.method, ledger_form.action, data_submit, 'application/x-www-form-urlencoded')
        });
        confirm("please do not flush or close the page")
        ajaxQueue.dequeue();
        // $.when(ajaxQueue).done(function () {
        //     document.getElementById("id_loader").setAttribute("class", "")
        //     alert("multipate job finished")
        // })

    })

};


// bootstrapTable formatter
function strFormatter(value, row) {
    return String(value)
  }

function fields_check(json_data, field_array) {
    field_array.forEach(field_name => {
        if (!(json_data.hasOwnProperty(field_name))) {
            return false
        }
    });
    return true
}


function get_select_value_option_text(select_id, option_text) {
    var selectElement = document.getElementById(select_id); // 通过id获取select元素
    var options = selectElement.options; // 获取所有选项

    for (var i = 0; i < options.length; i++) {
        var optionValue = options[i].value; // 获取每个选项的值
        var optionText = options[i].text; // 获取每个选项的文本内容
        // console.log("值：" + optionValue + "，文本：" + optionText);
        if (option_text == optionText) {
            return optionValue
        }
    }
    return ""
}

function formatTime(input) {
    const date = new Date(input);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
  
    return `${year}-${month}-${day} ${hours}:${minutes}`;
  }


  function queueAjaxRequest(type, url, data, dataType) {
    ajaxQueue.queue(function(next) {
        $.ajax({
            type: type,
            url: url,
            data: data,
            // async: false,
            dataType: dataType,
            beforeSend: function(xhr) {
                document.getElementById("load_parent").setAttribute("class", "loading-overlay");
                document.getElementById("id_loader").setAttribute("class", "loader");
                global_multipate_add_ajax_num += 1;
              },
            success: function(data) {
                // 请求成功后执行的操作
                console.log('AJAX request to ' + url + ' completed');
            },
            complete: function() {
                document.getElementById("id_loader").setAttribute("class", "");
                document.getElementById("load_parent").setAttribute("class", "")
                // 当前请求完成后，调用 next() 继续下一个请求
                next();
            }
        });
    });
}