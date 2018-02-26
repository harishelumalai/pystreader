const crypto = require('crypto');

module.exports = function(server, options) {
    const encode = function(pwd) {
        return crypto.createHash('sha256').update(pwd).digest('hex');
    };
    
    const create = function(request, reply) {
        
        if (request.auth.isAuthenticated) {
            return reply.continue();
        }

        let message;
        let username;
        let password;
        let repassword;
        let checked = false;
        let processing = true;
        
        let createForm = function(reply) {
            return reply('<!DOCTYPE html>' +
                '<html>' +
                '<head>' +
                '<title>Create User - Kibana</title>' +
                '<link rel="stylesheet" href="/bundles/commons.style.css">' +
                '<link rel="stylesheet" href="/bundles/kibana.style.css">' +
                '</head>' +
                '<body>' +
                '<center>' +
                '<div class="container" style="width: 20%;margin-left: auto;margin-right:auto;margin-top: 10%;">' +
                '<h1 style="background-color: #e8488b"><img width="60%" src="./kibana.png"></h1>' +
                (message ? '<h3>' + message + '</h3><br/>' : '') +
                '<form id="create-form" method="post" action="/create">' +
                '<div class="form-group inner-addon left-addon">' +
                '<input type="text" style="margin-bottom:8px;font-size: 1.25em;height: auto;" name="username" placeholder="Username" class="form-control">' +
                '<input type="password" style="margin-bottom:8px;font-size: 1.25em;height: auto;" name="password" placeholder="Password" class="form-control">' +
                '<input type="password" style="margin-bottom:8px;font-size: 1.25em;height: auto;" name="confirm_password" placeholder="Confirm Password" class="form-control">' +
                '</div><div style="width:200px;margin-left:auto;margin-right:auto;">' +
                '<input type="submit" value="Create User" class="btn btn-default login" style="width: 80%;font-size: 1.5em;">' +
                '</div>' +
                '</form>' +
                '</div>' +
                '</center>' +
                '</body>' +
                '</html>');
        }
            
        if (request.method === 'post') {
            username = request.payload.username;
            password = request.payload.password;
            repassword = request.payload.confirm_password;
        } else if (request.method === 'get') {
            username = request.query.username;
            password = request.query.password;
            repassword = request.payload.confirm_password;
        }

        if (!username && !password && !repassword && password !== repassword) {
            processing = false;
        }

        if (username || password || repassword) {
            //commenting for now. db doesnt have enc. pwd
            //let encPass = encode(password);

            //const { callWithRequest } = server.plugins.elasticsearch.getCluster('elasticsearch');
            const Cluster = server.plugins.elasticsearch.getCluster('data');
            
            //Check username availability
            Cluster.callWithRequest(request, 'request', {
                index: "users", //'users' index for testing. uname=admin,pwd=admin
                allowNoIndices: false,
                body: {
                    "size": 1,
                    "query": {
                        "match": {
                            "username": username
                        }
                    }
                }
            }).then(res => {
                if (res.hits.total == 0) {
                        checked = true;
			            console.log("Username available");
                        Cluster.callWithRequest(request, 'transport.request', {
                            path: '/users/user/',
                            method: 'POST',
                            body: {
                                "username" : username,
                                "password" : password
                            }
                        }).then(res1 => {
                            
                                processing = true;
                                message = 'New user created successfully.';
                                loginForm(reply);
                            }, 
                        function(error) { console.log('error in insertion'); message='error in insert'; createForm(reply);}
                        );
                        
                    } else {
                        message = 'Username already taken.';
                        createForm(reply);
                    }
            },
            function(error) {
                    checked = false;
                    message = 'Username already taken.(error)';
                    createForm(reply);
                });

        } else if (request.method === 'post') {
            processing = false;
            message = 'Missing username or password';
        }

        if (!checked && !processing) {
            createForm(reply);
        }
        
    };

    const login = function(request, reply) {

        if (request.auth.isAuthenticated) {
            return reply.continue();
        }

        let message;
        let username;
        let password;
        let checked = false;
        let processing = true;

        let loginForm = function(reply) {
            return reply('<!DOCTYPE html>' +
                '<html>' +
                '<head>' +
                '<title>Login Required</title>' +
                '<link rel="stylesheet" href="/bundles/commons.style.css">' +
                '<link rel="stylesheet" href="/bundles/kibana.style.css">' +
                '</head>' +
                '<body>' +
                '<center>' +
                '<div class="container" style="width: 20%;margin-left: auto;margin-right:auto;margin-top: 10%;">' +
                '<h1 style="background-color: #e8488b"><img width="60%" src="bundles/src/ui/public/images/kibana.svg"></h1>' +
                (message ? '<h3>' + message + '</h3><br/>' : '') +
                '<form id="login-form" method="post" action="/login">' +
                '<div class="form-group inner-addon left-addon">' +
                '<input type="text" style="margin-bottom:8px;font-size: 1.25em;height: auto;" name="username" placeholder="Username" class="form-control">' +
                '<input type="password" style="font-size: 1.25em;height: auto;" name="password" placeholder="Password" class="form-control">' +
                '</div><div style="width:200px;margin-left:auto;margin-right:auto;">' +
                '<input type="submit" value="Login" class="btn btn-default login" style="width: 80%;font-size: 1.5em;">' +
                '<a href="/create"></a>' +
                '</div>' +
                '</form>' +
                '</div>' +
                '</center>' +
                '</body>' +
                '</html>');

        };
        
        

        if (request.method === 'post') {
            username = request.payload.username;
            password = request.payload.password;
        } else if (request.method === 'get') {
            username = request.query.username;
            password = request.query.password;
        }

        if (!username && !password) {
            processing = false;
        }

        if (username || password) {
            //commenting for now. db doesnt have enc. pwd
            //let encPass = encode(password);

            //const { callWithRequest } = server.plugins.elasticsearch.getCluster('elasticsearch');
            const Cluster = server.plugins.elasticsearch.getCluster('data');
                Cluster.callWithRequest(request, 'search', {
                index: "users", //'users' index for testing. uname=admin,pwd=admin
                allowNoIndices: false,
                body: {
                    "size": 1,
                    "query": {
                        "match": {
                            "username": username
                        }
                    }
                }
            }).then(res => {
		//Change password into encPass
                if (res.hits.hits[0] && res.hits.hits[0]._source.password == password) {
                        checked = true;
			console.log("User authenticated");
                        let uuid = 1;
                        const sid = String(++uuid);
                        request.server.app.cache.set(sid, {
                            username: username
                        }, 0, (err) => {
                            if (err) {
                                reply(err);
                            }

                            request.auth.session.set({
                                sid: sid
                            });
                            // var auth = "Basic " + new Buffer(username + ":" + password).toString("base64");
                            return reply.redirect("/");
                        });
                    } else {
                        message = 'Invalid username or password';
                        loginForm(reply);
                    }
            },
            function(error) {
                    checked = false;
                    message = 'Invalid username or password';
                    loginForm(reply);
                });

        } else if (request.method === 'post') {
            processing = false;
            message = 'Missing username or password';
        }

        if (!checked && !processing) {
            loginForm(reply);
        }
    };

    const logout = function(request, reply) {
        request.auth.session.clear();
        return reply.redirect('/');
    };

    server.register(require('hapi-auth-cookie'), (err) => {
        const authHash = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
        const salt = "RJMIgyv5P8gxiylnd7z5vrHj3a91ILBe";
	
	console.log(authHash);

        if (err) {
            throw err;
        }

        const cache = server.cache({
            segment: 'sessions',
            expiresIn: 60 * 1000	//1 min
        });
        server.app.cache = cache;

        server.auth.strategy('session', 'cookie', true, {
            password: authHash + salt,
            cookie: 'sid',
            redirectTo: '/login',
            isSecure: false,
            validateFunc: function(request, session, callback) {


                cache.get(session.sid, (err, cached) => {

                    if (err) {
                        return callback(err, false);
                    }

                    if (!cached) {
                        return callback(null, false);
                    }

                    return callback(null, true, cached.username);
                });
            }
        });

        server.route([{
                method: ['GET', 'POST'],
                path: '/login',
                config: {
                    handler: login,
                    auth: {
                        mode: 'try'
                    },
                    plugins: {
                        'hapi-auth-cookie': {
                            redirectTo: false
                        }
                    }
                }
            },
            {
                method: 'GET',
                path: '/logout',
                config: {
                    handler: logout
                }
            },
            {
                method: ['GET','POST'],
                path: '/create',
                config: {
                    handler: create,
                    auth: {
                        mode: 'try'
                    },
                    plugins: {
                        'hapi-auth-cookie': {
                            redirectTo: false
                        }
                    }
                }
            }
        ]);
	
    });
};
