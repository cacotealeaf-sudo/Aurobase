// 定义要插入的HTML代码 
const sidemenu = `
  
`;
const contactform = `
  
`;
const footer=`

`
const contactpageform=`

`

// 获取页面中的容器元素
const sidemenubox = document.getElementById('colorlib-aside');
const popupbox = document.getElementById('pop-qform');
const footerbox = document.getElementById('footer-sec');
const contactpageformbox = document.getElementById('contactpage-form');
// 将innerHTML设置为要插入的HTML代码
if(sidemenubox){
	sidemenubox.innerHTML = sidemenu;
}
if(popupbox){
	popupbox.innerHTML = contactform;
}
if(footerbox){
	footerbox.innerHTML = footer;
}
if(contactpageformbox){
	contactpageformbox.innerHTML = contactpageform;
}


