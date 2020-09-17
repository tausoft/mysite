function readURL(input) {

    if (input.files && input.files[0]) {

    
        var reader = new FileReader();
  
        reader.onload = function(e) {
            $('.image-upload-wrap').hide();
            $('.file-upload-image').attr('src', e.target.result);
            $('.file-upload-content').show();
            $('.file-submit-content').show();
            
            $('.image-title').html(input.files[0].name);
        };
  
        reader.readAsDataURL(input.files[0]);
  
    } else {
        removeUpload();
    }
}
 
function removeUpload() {
    event.preventDefault();
    $('.file-upload-input').replaceWith($('.file-upload-input').val('').clone(true));
    $('.file-upload-content').hide();
    $('.file-submit-content').hide();
    $('.image-upload-wrap').removeClass('image-dropping');
    $('.image-upload-wrap').show();
}

$('.image-upload-wrap').bind('dragover', function () {
    $('.image-upload-wrap').addClass('image-dropping');
});

$('.image-upload-wrap').bind('dragleave', function () {
    $('.image-upload-wrap').removeClass('image-dropping');
});

function fnValidate(){
    if (ace_alert == 0){
        $('.ace-alert').fadeOut("slow");
    }
    if (ace_alert == 1){
        event.preventDefault();
        $('.ace-alert').fadeIn("slow");
    }
ace_alert = 1
}

function isIMEI(s) {
    var etal = /^[0-9]{15}$/;
    if (!etal.test(s))
        return '0';
    sum = 0; mul = 2; l = 14;
    for (i = 0; i < l; i++) {
        digit = s.substring(l-i-1,l-i);
        tp = parseInt(digit,10)*mul;
        if (tp >= 10)
            sum += (tp % 10) +1;
        else
            sum += tp;
        if (mul == 1)
            mul++;
        else
            mul--;
        }
    chk = ((10 - (sum % 10)) % 10);
    if (chk != parseInt(s.substring(14,15),10))
        return '1';
    return '2';
    }   

function searchValidate(){
    var x = document.getElementById("imei").value;
    if(isIMEI(x) == '0'){
        event.preventDefault();
        $('.not-luhn-input').hide();
        $('.not-numeric-input').hide();;
        $('.not-numeric-input').fadeIn("slow");
    }
    if(isIMEI(x) == '1'){
        event.preventDefault();
        $('.not-numeric-input').hide();
        $('.not-luhn-input').hide();
        $('.not-luhn-input').fadeIn("slow");
    }
    if(isIMEI(x) == '2'){
        $('.not-luhn-input').hide();
        $('.not-numeric-input').hide();
    }
}

function nokiaValidate(){
    var x = document.getElementById("proizvodjac").value;
    if (x == 'nokia' || proizvodjac_lwr == 'nokia'){
        $('.input-btn-hidden').show();
        $('.show-nokia').fadeIn("slow");
    }
    else{
        $('.input-btn-hidden').hide();
        $('.show-nokia').fadeOut("slow");
    }
}

function kontaktValidate(s){
    var etal = /^([0]{1})([6]{1})([0-9]{7})([0-9]{1})?$/;
    if (!etal.test(s)){
        return '0';
    }
    else{
        return '1';
    }
}

function proizvodjacValidate(s){
    var etal = "";
    if (!etal.test(s)){
        return '0';
    }
    else{
        return '1';
    }
}

function formValidate(){
    var x = document.getElementById("kontakt").value;{
        if(kontaktValidate(x) == '1'){
            $('.kontakt-alert').hide();
            $('.empty-kontakt-alert').hide();
        }
        if(kontaktValidate(x) == '0'){
            event.preventDefault();
            if(x == ''){
                event.preventDefault();
                $('.kontakt-alert').hide();
                $('.empty-kontakt-alert').hide();
                $('.empty-kontakt-alert').fadeIn("slow");
            }
            else{
                $('.empty-kontakt-alert').hide();
                $('.kontakt-alert').hide();
                $('.kontakt-alert').fadeIn("slow");
            }
        }
    }
    var y = document.getElementById("proizvodjac").value;
    var q = document.getElementById("model").value;{
        if(q == ''){
            $('.proizvodjac-alert').hide();
            $('.nokia-model-alert').hide();
        }
        if(q == '' && y == 'nokia'){
            event.preventDefault();
            $('.proizvodjac-alert').hide();
            $('.nokia-model-alert').hide();
            $('.nokia-model-alert').fadeIn("slow");
        }
        if(y != '' && y != 'nokia'){
            document.getElementById("model").value = '';
            $('.nokia-model-alert').hide();
            $('.proizvodjac-alert').hide();
        }
        if(y == '' && y != 'nokia'){
            event.preventDefault();
            $('.nokia-model-alert').hide();
            $('.proizvodjac-alert').hide();
            $('.proizvodjac-alert').fadeIn("slow");
        }
        if(q != '' && y == 'nokia'){
            $('.nokia-model-alert').hide();
            $('.proizvodjac-alert').hide();
        }
    }
    var z = document.getElementById("imei").value;{
        if(isIMEI(z) == '0'){
            event.preventDefault();
            $('.not-luhn-input').hide();
            $('.not-numeric-input').hide();
            $('.not-numeric-input').fadeIn("slow");
        }
        if(isIMEI(z) == '1'){
            event.preventDefault();
            $('.not-numeric-input').hide();
            $('.not-luhn-input').hide();
            $('.not-luhn-input').fadeIn("slow");
        }
        if(isIMEI(z) == '2'){
            $('.not-luhn-input').hide();
            $('.not-numeric-input').hide();
        }
    }
}

function deleteValidate(){
    if (confirm("Da li ste sigurni da želite da obrišete unos?")) {
    } 
    else {
        event.preventDefault();
    }
}

function toggleAll(source) {
    checkboxes = document.getElementsByClassName('select_all');
    for(var i=0, n=checkboxes.length;i<n;i++) {
      checkboxes[i].checked = source.checked;
    }
}


function checkboxChecker() {
    var result = false;
    checkboxes = document.getElementsByClassName('select_all');
    for(var i=0, n=checkboxes.length;i<n;i++) {
        if(checkboxes[i].checked == true){
            result = true;
            break;
        }
        else{
            result = false
        }
    }
    if(result == true){
        $('.checkbox-alert').fadeOut("slow");
    }
    else{
        event.preventDefault();
        $('.checkbox-alert').fadeIn("slow");
    }
}






getPagination('#table-id');
//getPagination('.table-class');
//getPagination('table');

/*					PAGINATION 
- on change max rows select options fade out all rows gt option value mx = 5
- append pagination list as per numbers of rows / max rows option (20row/5= 4pages )
- each pagination li on click -> fade out all tr gt max rows * li num and (5*pagenum 2 = 10 rows)
- fade out all tr lt max rows * li num - max rows ((5*pagenum 2 = 10) - 5)
- fade in all tr between (maxRows*PageNum) and (maxRows*pageNum)- MaxRows 
*/

function getPagination (table){

var lastPage = 1 ; 

$('#maxRows').on('change',function(evt){
//$('.paginationprev').html('');						// reset pagination 


lastPage = 1 ; 
$('.pagination').find("li").slice(1, -1).remove();
var trnum = 0 ;									// reset tr counter 
var maxRows = parseInt($(this).val());			// get Max Rows from select option

if(maxRows == 5000 ){

$('.pagination').hide();
}else {

$('.pagination').show();
}

var totalRows = $(table+' tbody tr').length;		// numbers of rows 
$(table+' tr:gt(0)').each(function(){			// each TR in  table and not the header
trnum++;									// Start Counter 
if (trnum > maxRows ){						// if tr number gt maxRows
 
 $(this).hide();							// fade it out 
}if (trnum <= maxRows ){$(this).show();}// else fade in Important in case if it ..
});											//  was fade out to fade it in 
if (totalRows > maxRows){						// if tr total rows gt max rows option
var pagenum = Math.ceil(totalRows/maxRows);	// ceil total(rows/maxrows) to get ..  
                                         //	numbers of pages 
for (var i = 1; i <= pagenum ;){			// for each page append pagination li 
$('.pagination #prev').before('<li data-page="'+i+'">\
                  <span>'+ i++ +'<span class="sr-only">(current)</span></span>\
                </li>').show();
}											// end for i 
} 												// end if row count > max rows
$('.pagination [data-page="1"]').addClass('active'); // add active class to the first li 
$('.pagination li').on('click',function(evt){		// on click each page
evt.stopImmediatePropagation();
evt.preventDefault();
var pageNum = $(this).attr('data-page');	// get it's number

var maxRows = parseInt($('#maxRows').val());			// get Max Rows from select option

if(pageNum == "prev" ){
if(lastPage == 1 ){return;}
pageNum  = --lastPage ; 
}
if(pageNum == "next" ){
if(lastPage == ($('.pagination li').length -2) ){return;}
pageNum  = ++lastPage ; 
}

lastPage = pageNum ;
var trIndex = 0 ;							// reset tr counter
$('.pagination li').removeClass('active');	// remove active class from all li 
$('.pagination [data-page="'+lastPage+'"]').addClass('active');// add active class to the clicked 
// $(this).addClass('active');					// add active class to the clicked 
$(table+' tr:gt(0)').each(function(){		// each tr in table not the header
 trIndex++;								// tr index counter 
 // if tr index gt maxRows*pageNum or lt maxRows*pageNum-maxRows fade if out
 if (trIndex > (maxRows*pageNum) || trIndex <= ((maxRows*pageNum)-maxRows)){
     $(this).hide();		
 }else {$(this).show();} 				//else fade in 
}); 										// end of for each tr in table
});										// end of on click pagination list

}).val(5).change();

                            // end of on select change 



            // END OF PAGINATION 
}	



$(function(){
// Just to append id number for each row  
$('table tr:eq(0)').prepend('<th></th>')

var id = 0;

$('table tr:gt(0)').each(function(){	
    id++
    $(this).prepend('<td></td>');
});
})


