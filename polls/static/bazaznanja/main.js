var ids = [];



function readURL(input) {
  var fileType = input.files[0].name.slice(input.files[0].name.length - 4);

  if (fileType == '.csv'){
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
  } else {
    alert('\nDatoteka ' + input.files[0].name + ' nije podržana!\n\nAplikacija podržava isključivo .csv (Comma-separated values) datoteke. Za potrebe masovnog unosa kodova potrebno je pripremiti adekvatnu datoteku koju čini sadržaj u formatu "IMEI,NCK" ili "IMEI;NCK".');
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

function myFunction() {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}

function detectIEEdge() {
  var ua = window.navigator.userAgent;
  var isIE = /MSIE|Trident/.test(ua);

  if ( isIE ) {
    alert('IE')
  } else {
    alert('not IE')
  }
}


// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
function myModal() {
  var modal = document.getElementById("myModal");
  var span = document.getElementsByClassName("close")[0];
  modal.style.display = "block";
  modal.style.cursor = "default";

  // When the user clicks on <span> (x), close the modal
  span.onclick = function() {
    modal.style.display = "none";
  }

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
  if (event.target == modal) {
      modal.style.display = "none";
      modal.style.cursor = "pointer";
      }
  }

  window.addEventListener('keydown', function (event) {
  if (event.key === 'Escape') {
      modal.style.display = 'none';
      modal.style.cursor = "pointer";
      }
  })
}


$(document).ready(function() {
  $('.newmessagebtn').on('click', function (e) {
      event.preventDefault();

        var user = $('#user').val();
        var imei = $('#imei').val();
        var group = $('#group').val();
        var level = $('#level').val();

        $.ajax({
          url: '/ajax/search_unc_ajax/',
          data: {
            'level': level,
            'user': user,
            'imei': imei,
            'group': group
          },
          dataType: 'json',
          success: function (data) {


            var x = document.getElementById("imei").value;
            if(x == ''){
        event.preventDefault();
        $('.not-luhn-input').hide();
        $('.not-numeric-input').hide();
        $('.imei-alert').hide();
        $('.imei-alert').fadeIn("slow");
      }
      else {
          if(isIMEI(x) == '0'){
              event.preventDefault();
              $('.not-luhn-input').hide();
              $('.not-numeric-input').hide();
              $('.imei-alert').hide();
              $('.not-numeric-input').fadeIn("slow");
          }
          if(isIMEI(x) == '1'){
              event.preventDefault();
              $('.not-numeric-input').hide();
              $('.not-luhn-input').hide();
              $('.imei-alert').hide();
              $('.not-luhn-input').fadeIn("slow");
          }
          if(isIMEI(x) == '2'){
              $('.not-luhn-input').hide();
              $('.not-numeric-input').hide();
              $('.imei-alert').hide();


              var modal = document.getElementById("myModal");
              var span = document.getElementsByClassName("close")[0];
              modal.style.display = "block";
              modal.style.cursor = "default";
              var level = data.level

              // append unlock list
              var unlock = data.unlock_list;
              var text = "";
              var i;
              for (i = 0; i < unlock.length; i++) {
                text += "<b>" + unlock[i] + "</b><br/>";
              }
              document.getElementById("o").innerHTML = text;
              // append unlock list


              // append imei string
              var text = data.imei_query;

              document.getElementById("p").innerHTML = text;
              // append imei string


              // append request pending
              if(level != 'level_3'){
                var text = data.unlock_not_found;
                if(text != ''){
                  document.getElementById("i").innerHTML = text;
                  $('#div_pending').fadeIn("slow");
                } else {
                  document.getElementById("i").innerHTML = '';
                  $('#div_pending').hide();
                }
              }
              // append request pending


              // append nokia winlock
              if(level == 'level_1'){
                var proizvodjac = data.proizvodjac_temp;
                var winlock = data.winlockpreview;
                if (proizvodjac == 'Nokia'){
                  document.getElementById("r").innerHTML = winlock;
                  $('#div_winlock').fadeIn("slow");
                } else {
                  document.getElementById("r").innerHTML = '';
                  $('#div_winlock').hide();
                }
              }
              // append nokia winlock


              // validate
              if(level != 'level_3'){
                var validation = data.validate;

                if(validation == 0){
                  $('#validate_0').fadeIn("slow");
                  $('#validate_1').hide();
                  $('#validate_3').hide();
                } else if(validation == 1 || validation == 5){
                  $('#validate_0').hide();
                  $('#validate_1').fadeIn("slow");
                  $('#validate_3').hide();
                } else if(validation == 3){
                  $('#validate_0').hide();
                  $('#validate_1').hide();
                  $('#validate_3').fadeIn("slow");
                } else {
                  $('#validate_0').hide();
                  $('#validate_1').hide();
                  $('#validate_3').hide();
                }
              }
              // validate


              // submit request
              if(level != 'level_3'){
                $('#imeihidden_0').val(data.imei_temp)
                $('#proizvodjachidden_0').val(data.proizvodjac_temp)
                $('#modelhidden_0').val(data.model_temp)
                $('#imeihidden_1').val(data.imei_temp)
                $('#proizvodjachidden_1').val(data.proizvodjac_temp)
                $('#modelhidden_1').val(data.model_temp)
                $('#imeihidden_3').val(data.imei_temp)
                $('#proizvodjachidden_3').val(data.proizvodjac_temp)
                $('#modelhidden_3').val(data.model_temp)
              }
              // submit request


              // When the user clicks on <span> (x), close the modal
              span.onclick = function() {
                modal.style.display = "none";
              }

              // When the user clicks anywhere outside of the modal, close it
              window.onclick = function(event) {
              if (event.target == modal) {
                  modal.style.display = "none";
                  modal.style.cursor = "pointer";
                  }
              }

              window.addEventListener('keydown', function (event) {
              if (event.key === 'Escape') {
                  modal.style.display = 'none';
                  modal.style.cursor = "pointer";
                  }
              })
            }
      }
          }
        });
      });
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
  if(x == ''){
        event.preventDefault();
        $('.not-luhn-input').hide();
        $('.not-numeric-input').hide();
        $('.imei-alert').hide();
        $('.imei-alert').fadeIn("slow");
      }
      else {
          if(isIMEI(x) == '0'){
              event.preventDefault();
              $('.not-luhn-input').hide();
              $('.not-numeric-input').hide();
              $('.imei-alert').hide();
              $('.not-numeric-input').fadeIn("slow");
          }
          if(isIMEI(x) == '1'){
              event.preventDefault();
              $('.not-numeric-input').hide();
              $('.not-luhn-input').hide();
              $('.imei-alert').hide();
              $('.not-luhn-input').fadeIn("slow");
          }
          if(isIMEI(x) == '2'){
              $('.not-luhn-input').hide();
              $('.not-numeric-input').hide();
              $('.imei-alert').hide();
          }
      }
}

function nokiaValidate(){
  var x = document.getElementById("proizvodjac").value;

  if (x == 'Nokia'){
      $('.input-btn-hidden').show();
      $('.show-nokia').fadeIn("slow");
  }
  else{
      $('.input-btn-hidden').hide();
      $('.show-nokia').fadeOut("slow");
  }

  if (x == ''){
    document.getElementById("proizvodjac").style.color = "gray";
  }
  else {
    document.getElementById("proizvodjac").style.color = "black";
  }
}

function modelColor(){
  var x = document.getElementById("model").value;
  if (x == ''){
    document.getElementById("model").style.color = "gray";
  }
  else {
    document.getElementById("model").style.color = "black";
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
      if(q == '' && y == 'Nokia'){
          event.preventDefault();
          $('.proizvodjac-alert').hide();
          $('.nokia-model-alert').hide();
          $('.nokia-model-alert').fadeIn("slow");
      }
      if(y != '' && y != 'Nokia'){
          document.getElementById("model").value = '';
          $('.nokia-model-alert').hide();
          $('.proizvodjac-alert').hide();
      }
      if(y == '' && y != 'Nokia'){
          event.preventDefault();
          $('.nokia-model-alert').hide();
          $('.proizvodjac-alert').hide();
          $('.proizvodjac-alert').fadeIn("slow");
      }
      if(q != '' && y == 'Nokia'){
          $('.nokia-model-alert').hide();
          $('.proizvodjac-alert').hide();
      }
  }
  var z = document.getElementById("imei").value;{
      if(z == ''){
        event.preventDefault();
        $('.not-luhn-input').hide();
        $('.not-numeric-input').hide();
        $('.imei-alert').hide();
        $('.imei-alert').fadeIn("slow");
      }
      else {
          if(isIMEI(z) == '0'){
              event.preventDefault();
              $('.not-luhn-input').hide();
              $('.not-numeric-input').hide();
              $('.imei-alert').hide();
              $('.not-numeric-input').fadeIn("slow");
          }
          if(isIMEI(z) == '1'){
              event.preventDefault();
              $('.not-numeric-input').hide();
              $('.not-luhn-input').hide();
              $('.imei-alert').hide();
              $('.not-luhn-input').fadeIn("slow");
          }
          if(isIMEI(z) == '2'){
              $('.not-luhn-input').hide();
              $('.not-numeric-input').hide();
              $('.imei-alert').hide();
          }
      }
  }
}

function toggleAll(source) {
  checkboxes = document.getElementsByClassName('select_all');
  for(var i=0, n=checkboxes.length;i<n;i++) {
    checkboxes[i].checked = source.checked;
  }
}


function checkboxChecker() {
  checkboxes = document.getElementById('selected').value;
    if(checkboxes != ''){
        $('.checkbox-alert').fadeOut("slow");
    }
    else{
        event.preventDefault();
        $('.checkbox-alert').fadeIn("slow");
    }
}



function selectMeMain(clicked_id){
    var selected = document.getElementById(clicked_id);
    var selectall = document.getElementById('selectall');
    var selectedall = document.getElementsByName('vendors');

    if(selected.classList.contains('select_notselected')){
        selected.classList.add('select_selected');
        selected.classList.remove('select_notselected');
        ids.push(clicked_id);
        document.getElementById("selected").value = ids;
    } else if(selected.classList.contains('select_selected')) {
        selected.classList.add('select_notselected');
        selected.classList.remove('select_selected');
        ids = ids.filter(e => e !== clicked_id);
        document.getElementById("selected").value = ids;
    }


    // document.getElementById('xlen').innerHTML = x.length
    // document.getElementById('selectalllen').innerHTML = selectedall.length

    if(selectedall.length != ids.length){
        selectall.classList.add('selectall_notselected');
        selectall.classList.remove('selectall_selected');
    } else {
        selectall.classList.add('selectall_selected');
        selectall.classList.remove('selectall_notselected');
    }
}

function selectAll() {
    var selectall = document.getElementById('selectall');
    var selectedall = document.getElementsByName('vendors');
    var x = [];

    if(selectedall.length != ids.length){
        var i;
        for (i = 0; i < selectedall.length; i++){
            selectedall[i].classList.add('select_selected');
            selectedall[i].classList.remove('select_notselected');
            selectall.classList.add('selectall_selected');
            selectall.classList.remove('selectall_notselected');
            x.push(selectedall[i].id)
            ids = x;
            document.getElementById("selected").value = x;
        }
    } else if(selectedall.length == ids.length) {
        var i;
        for (i = 0; i < selectedall.length; i++){
            selectedall[i].classList.add('select_notselected');
            selectedall[i].classList.remove('select_selected');
            selectall.classList.add('selectall_notselected');
            selectall.classList.remove('selectall_selected');
            x = [];
            ids = [];
            document.getElementById("selected").value = x;
        }
    }
}






