let nav = document.getElementsByClassName("global-nav__links-section")[1];
if ( nav !== undefined ) {
    let nav1 = nav.getElementsByClassName("global-nav-link")[0];
    //window.alert(nav + "---" + nav1);
}

var observer = new MutationObserver(function (m) {
    m.forEach(function(entry) {
        console.log("foreach m");
        console.log(m);
        entry.addedNodes.forEach(function (addednode) {
            console.log("added node");
            console.log(addednode);
            let nav2 = addednode.getElementsByClassName("global-nav__links-section")[1];
            if ( nav2 !== undefined ) {
                let nav3 = nav2.getElementsByClassName("global-nav-link")[0];
                //window.alert(nav2 + "---" + nav3);
                if( addednode.getElementsByClassName("global-nav__links-section")[1].getElementsByClassName("global-nav-link")[0] !== undefined)
                {
                    console.log("Kibana Nav links loaded. Now inject code");
                    //create logout button here
                    
                    //var div= wrapper.firstChild;
                    //add button before collapse
                    var logout= document.createElement('div');
                    logout.className = "global-nav-link";
                    logout.innerHTML= '<a class="global-nav-link__anchor" href="/logout" title="Logout"><div class="global-nav-link__icon"><img class="global-nav-link__icon-image" src="/plugins/kibana/assets/logout.svg"></div><div class="global-nav-link__title">Logout</div></a>';
                    
                    //document.getElementsByClassName("global-nav__links-section")[1].getElementsByClassName("global-nav-link")[0].appendChild(document.createElement("a").appendChild(document.createTextNode("logout")));
                    document.getElementsByClassName("global-nav__links-section")[1].getElementsByClassName("global-nav-link")[0].appendChild(logout);
                    observer.unobserve();
                    
                }
            }
        });
    })
});
observer.observe(document.body, {childList: true});
