// reveal content on profile page

const rBtn = document.querySelector("#reveal-btn")
const hiddenContent = document.querySelector(".hidden")


function revealContent() {
	if(hiddenContent.classList.contains('reveal-content')) {
		hiddenContent.classList.remove('reveal-content')
	} else {
		hiddenContent.classList.add('reveal-content')
	}
}

rBtn.addEventListener('click', revealContent);



CKEDITOR.plugins.addExternal( 'filebrowser', '/static/ckeditor/filebrowser/', 'plugin.js' );
CKEDITOR.config.extraPlugins = 'filebrowser';
CKEDITOR.config.filebrowserBrowseUrl  = '/upload';