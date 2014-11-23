function init_editor() {
    new Vue({
        el: '#editor',
        data: {
            input: '# hello'
        },
        filters: {
            marked: weasyl
        }
    });
}

function weasyl(input) {

    input = weasylUsernames(input);
    input = marked(input);
    return input
}

function weasylUsernames(input) {
    // Weasyl user icons
    var icon_regex = /<(!~|!)(..:)?(\w+)>/mgi;
    var match = icon_regex.exec(input);
    while (match != null) {
        var img;
        var link;
        switch (match[2]) {
            case 'fa:':
                img = 'https://a.facdn.net/' + match[3] + '.gif';
                link = 'https://www.furaffinity.net/user/' + match[3];
                break;

            default:
                img = 'https://www.weasyl.com/~' + match[3] + '/avatar';
                link = 'https://www.weasyl.com/~'+ match[3];
        }

        var tail = '';
        if (match[1] == '!~') {
            tail = match[3];
        }
        input = input.replace(match[0],
            '<a href="'+link+'"><img src="'+img+'" style="height: 50px"></img> '+tail+'</a>');
        match = icon_regex.exec(input);
    }

    var username_regex = /<(!~|[!~])(..:)?(\w+)>/gi;
    var match = username_regex.exec(input);
    while (match != null) {
        var link;
        switch (match[2]) {
            case 'fa:':
                link = 'https://www.furaffinity.net/user/' + match[3];
                break;

            case 'da:':
                link = 'https://' + match[3] + '.deviantart.com/';
                break;

            case 'sf:':
                link = 'https://' + match[3] + '.sofurry.com/';
                break;

            case 'ib:':
                link = 'https://inkbunny.net/' +match[3];
                break;

            default:
                link = 'https://www.weasyl.com/~' + match[3];
        }

        input = input.replace(match[0], '<a href="'+link+'">'+match[3]+'</a>')
        match = username_regex.exec(input);
    }


    return input;
}


/*
var weasylMarkdown = (function () {
    var USER_LINK = /\\(.)|<(!~|[!~])(\w+)>|./gi;

    var NO_USER_LINKING = ['a', 'pre', 'code'];

    function addUserLinks(fragment) {
        for (var i = 0; i < fragment.childNodes.length; i++) {
            var child = fragment.childNodes[i];

            if (child.nodeType === 1) {
                if (NO_USER_LINKING.indexOf(child.nodeName) === -1) {
                    addUserLinks(child);
                }
            } else if (child.nodeType === 3) {
                var m;
                var text = '';
                var altered = false;

                while ((m = USER_LINK.exec(child.nodeValue))) {
                    if (m[1] !== undefined) {
                        text += m[1];
                        altered = true;
                        continue;
                    }

                    if (m[2] === undefined) {
                        text += m[0];
                        continue;
                    }

                    altered = true;

                    var link = document.createElement('a');
                    link.href = '/~' + loginName(m[3]);

                    if (m[2] === '~') {
                        link.textContent = m[3];
                    } else {
                        link.className = 'user-icon';

                        var image = document.createElement('img');
                        image.src = '/~' + loginName(m[3]) + '/avatar';
                        link.appendChild(image);

                        if (m[2] === '!') {
                            image.alt = m[3];
                        } else {
                            var usernameContainer = document.createTextNode('span');
                            usernameContainer.textContent = m[3];

                            link.appendChild(document.createTextNode(' '));
                            link.appendChild(usernameContainer);
                        }
                    }

                    fragment.insertBefore(document.createTextNode(text), child);
                    fragment.insertBefore(link, child);
                    text = '';
                }

                if (altered) {
                    fragment.insertBefore(document.createTextNode(text), child);
                    i = Array.prototype.indexOf.call(fragment.childNodes, child) - 1;
                    fragment.removeChild(child);
                }
            }
        }
    }

    function weasylMarkdown(fragment) {
        var links = fragment.getElementsByTagName('a');

        forEach(links, function (link) {
            var href = link.getAttribute('href');
            var i = href.indexOf(':');
            var scheme = href.substring(0, i);
            var user = href.substring(i + 1);

            switch (scheme) {
                case 'user':
                    link.href = '/~' + user;
                break;

                case 'da':
                    link.href = 'https://' + user + '.deviantart.com/';
                break;

                case 'sf':
                    link.href = 'https://' + user + '.sofurry.com/';
                break;

                case 'ib':
                    link.href = 'https://inkbunny.net/' + user;
                break;

                case 'fa':
                    link.href = 'https://www.furaffinity.net/user/' + user;
                break;

                default:
                    return;
            }

            if (!link.textContent || link.textContent === href) {
                link.textContent = user;
            }
        });

        var images = fragment.querySelectorAll('img');

        forEach(images, function (image) {
            var src = image.getAttribute('src');
            var i = src.indexOf(':');
            var scheme = src.substring(0, i);
            var link = document.createElement('a');

            if (scheme === 'user') {
                var user = src.substring(i + 1);
                image.className = 'user-icon';
                image.src = '/~' + user + '/avatar';

                link.href = '/~' + user;

                image.parentNode.replaceChild(link, image);
                link.appendChild(image);

                if (image.alt) {
                    link.appendChild(document.createTextNode(' ' + image.alt));
                    image.alt = '';
                } else {
                    image.alt = user;
                }

                if (image.title) {
                    link.title = image.title;
                    image.title = '';
                }
            } else {
                link.href = image.src;
                link.appendChild(document.createTextNode(image.alt || image.src));

                image.parentNode.replaceChild(link, image);
            }
        });

        addUserLinks(fragment);
    }

    return weasylMarkdown;
});

var markdownOptions = {
    breaks: true,
    smartLists: true
};

var ATTEMPTED_BBCODE = /\[(\w+)\][\s\S]+\[\/\1\]/i;

function renderMarkdown(content, container) {
    var markdown = marked(content, markdownOptions);
    var fragment = document.createElement('div');
    fragment.innerHTML = markdown;

    weasylMarkdown(fragment);
    defang(fragment);

    while (fragment.childNodes.length) {
        container.appendChild(fragment.firstChild);
    }
}

function addMarkdownPreview(input) {
    var preview = document.createElement('div');
    preview.className = 'markdown-preview formatted-content';

    function showPreview() {
        while (preview.childNodes.length) {
            preview.removeChild(preview.firstChild);
        }

        renderMarkdown(input.value, preview);
    }

    input.addEventListener('input', showPreview, false);

    showPreview();
    input.parentNode.insertBefore(preview, input.nextSibling);
}
*/
