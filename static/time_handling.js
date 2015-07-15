function replaceTimeStamps(){
    $('.timestamps').each(function(i, el){
        var remainingTime = moment($(el).attr("data-time")).fromNow();
        // Just to reload all info, I know it's a bit crappy ^^"
        if(moment() > moment($(el).attr("data-time"))){
            location.reload();
        }
        $(el).text(remainingTime);
    });
};

$(document).ready(function(){
    replaceTimeStamps();
    setInterval(replaceTimeStamps, 10000)
});

