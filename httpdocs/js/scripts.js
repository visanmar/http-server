window.addEventListener('load', () => {
	cookieList = document.getElementById('cookieList')
	cookies = document.cookie.split('; ')
	
	cookieList.innerHTML = ''
	for (c in cookies) {
		cookie = cookies[c].split('=')
		if (cookie[0] == 'testcookie2')
			cookie[1] = 'new-value'
		cookies[c] = cookie.join('=')
		cookieList.innerHTML += `<div>${cookie}</div>`
	}
	cookies = cookies.join('; ')
	console.log(cookies)
	document.cookie = cookies
})

function testjs() {
	//alert('test javascript')
	
	fetch('http://localhost:65432/test_folder/test.json')
		.then( resp => resp.json() )
		.then( data => console.log(data) )
	
}