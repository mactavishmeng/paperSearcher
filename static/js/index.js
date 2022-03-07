const $table = $('#table');
const source_pool = {
    "ccs": "Computer and Communications Security (CCF A)",
    "sp": "IEEE Symposium on Security and Privacy (CCF A)",
    "spw": "International Security Protocols Workshop (CCF None)",
    "uss": "USENIX Security Symposium (CCF A)",
    "cest": "CSET @ USENIX Security Symposium (CCF None)",
    "foci": "FOCI @ USENIX Security Symposium (CCF None)",
    "soups": "SOUPS @ USENIX Security Symposium (CCF C)",
    "woot": "WOOT @ USENIX Security Symposium (CCF None)",
    "tdsc": "IEEE Transactions on Dependable and Secure Computing (CCF A)",
    "tifs": "IEEE Transactions on Information Forensics and Security (CCF A)",
    "ndss": "Network and Distributed System Security Symposium (CCF B)",
    "acsac": "Annual Computer Security Applications Conference (CCF B)",
    "csur": "ACM Computing Surveys (CCF None)",
    "comsur": "IEEE Communications Surveys and Tutorials (CCF None)",
    "esorics": "European Symposium on Research in Computer Security (CCF B)",
    "csfw": "IEEE Computer Security Foundations Symposium (CCF B)",
    "dsn": "Dependable Systems and Networks (CCF B)",
    "compsec": "Computers & Security (CCF B)",
    "raid": "International Symposium on Recent Advances in Intrusion Detection (CCF B)",
    "jcs": "Journal of Computer Security (CCF B)",
    "tissec": "ACM Transactions on Privacy and Security (CCF B)",
    "srds": "IEEE International Symposium on Reliable Distributed Systems (CCF B)"
};

// 给关键字上色
const getKeywords = function (query) {
    let i = 0;
    let finish_flag = false;
    let tmp = "";
    let keywords = [];

    while (i <= query.length) {
        if (i == query.length) finish_flag = true;
        // 遇到逻辑符号停止
        else if (query[i] == "+" || query[i] == "|") finish_flag = true
        // 将下一个字符添加到tmp
        else tmp += query[i];

        if (finish_flag) {
            // 如果去空格之后不为空字符串，就添加到keyword列表
            tmp = tmp.trim()
            if (tmp) keywords.push(tmp);
            tmp = "";
            finish_flag = false;
        }
        i++;
    }
    return keywords;
};


$(function (){
    // 绑定搜索按钮
    $('#search').click(function (){
        // 去掉table的隐藏
        $("#table").removeAttr("hidden");

        // 拼接搜索链接
        const query = $("#keyword").val();
        const req_rul  = "./search?q=" + encodeURIComponent(query)

        // 先destroy，再重建表格对象
        $table.bootstrapTable('destroy');
        $table.bootstrapTable({
            sidePagination : 'server',
            url: req_rul,
            // 设置加载完成的绑定事件，否则tooltip不工作
            onLoadSuccess: function (data) {
                $('[data-toggle="tooltip"]').tooltip()
                // 刷新 mathjax 状态
                MathJax.startup.defaultReady();
                MathJax.startup.promise.then(() => {
                    console.log('MathJax initial typesetting complete');
                });
                // 滚动到新页面的第一行
                $('html,body').animate({ scrollTop: $("#title-area").height() }, 500);
            }
        })
    })
})

function operateFormatter(value, row, index) {
    // 拼接工具栏
    return [
        '<span class="badge badge-primary" data-toggle="tooltip" data-placement="bottom" title="',
        source_pool[row['conf']],
        '">',
        row['conf'],
        '</span> ',
        '<span class="badge badge-success">',
        row['year'],
        '</span> ',
        '<span class="badge badge-secondary">',
        row['cat'],
        '</span> ',
        '<a class="badge badge-light" target="_blank" href="',
        row['href'],
        '"><i class="fas fa-globe"></i> Web</a>',
        '<a class="badge badge-light" target="_blank" href="',
        row['bib'],
        '"><i class="fas fa-edit"></i>Cite</a>',
        '<a class="badge badge-light view_abstract" article-id="',
        row['id'],
        '"><i class="fas fa-eye"></i>Abstract</a>',
    ].join("")
}

function titleFormatter(value, row, index) {
    // 为 title 设置样式（主要是关键字高亮）
    const kw = getKeywords($("#keyword").val());
    let title_content = value
    for(const key in kw) {
        const regS = new RegExp(kw[key], "ig");
        title_content = title_content.replace(regS, "<b>$&</b>")
    }
    return [
        "<h4>",
        title_content,
        "</h4>"
    ].join("")
}

window.operateEvents = {
    // 为 abstract 按钮绑定点击事件
    'click .view_abstract': function (e, value, row, index) {
        const query = $("#keyword").val();
        const article_id = row['id'];
        $.get("./abstract/" + article_id, function (data, status) {
            const content = $.parseJSON(data);
            let title = content['data'][0][0];
            let body = content['data'][0][1].replace('\n<', '<').replace('>\n', '>');

            // 替换关键词为高亮
            const kw = getKeywords(query);
            for (const key in kw) {
                const regS = new RegExp(kw[key], "ig");
                body = body.replace(regS, "<b>$&</b>")
                title = title.replace(regS, "<b>$&</b>")
            }
            $("#modal—title").html(title);
            $("#abstract_text").html(body.replace('\n', '<br>'));
            $('#myModal').modal('show');

            // 刷新 mathjax 状态
            MathJax.startup.defaultReady();
            MathJax.startup.promise.then(() => {
                console.log('MathJax initial typesetting complete');
            });
        });
    },
}

