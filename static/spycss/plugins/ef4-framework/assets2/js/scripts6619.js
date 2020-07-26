/**
 * Created by Admin on 6/29/2018.
 */

// field element
jQuery(function ($) {
    //Flatpicker plugin
    $('.flatpickr-date').each(function () {
        var $this = $(this);
        var option = {dateFormat: "Y-m-d",};
        var min = $this.attr('data-min');
        if (min) {
            option['minDate'] = min;
        }
        $this.flatpickr(option);
    });
    $('.flatpickr-datetime').each(function () {
        var $this = $(this);
        var option = {
            enableTime: true,
            dateFormat: "Y-m-d H:i",
        };
        var min = $this.attr('data-min');
        if (min) {
            option['minDate'] = min;
        }
        $this.flatpickr(option);
    });
    $('.flatpickr-timepicker').each(function () {
        var $this = $(this);
        var option = {
            enableTime: true,
            noCalendar: true,
            dateFormat: "H:i",
        };
        $this.flatpickr(option);
    });
});

//form action
String.prototype.trimLeft = function (charlist) {
    if (charlist === undefined)
        charlist = "\s";

    return this.replace(new RegExp("^[" + charlist + "]+"), "");
};
String.prototype.trimRight = function (charlist) {
    if (charlist === undefined)
        charlist = "\s";

    return this.replace(new RegExp("[" + charlist + "]+$"), "");
};
String.prototype.trim = function (charlist) {
    return this.trimLeft(charlist).trimRight(charlist);
};


EF4Dependency = function () {
    var $this = this;
    var el_reg = new RegExp('el{([^{}]+)}');
    // el{[name=""]} {=} abc {&&}
    var compare_reg = new RegExp('{[*!=]+}');
    var match_reg = new RegExp('{[&|]+}');
    var compare = {
        '!=': function (a, b) {
            return $this.get_val(a) != $this.get_val(b);
        },
        '*=': function (a, b) {
            console.log('check',[$this.get_val(a),b]);
            return $this.get_val(a).indexOf(b) != -1;
        },
        '=': function (a, b) {
            return $this.get_val(a) == $this.get_val(b);
        }
    };
    var match = {
        '&&': function (a, b) {
            return !!($this.compare(a) && $this.compare(b));
        },
        '||': function (a, b) {
            return !!($this.compare(a) || $this.compare(b));
        }
    };
    $this.get_attach_element_selector = function (query) {
        var result = [],current_query = query,check;
        for(var i = 0;i<current_query.length;i++)
        {
            check = el_reg.exec(current_query);
            if(!check)
                break;
            result.push(check[1]);
            current_query = current_query.replace(check[0],'');
        }
        return result;
    };
    $this.get_val = function (query) {
       var value = query;
       var try_take_el = el_reg.exec(query);
       if(try_take_el){
           var element = jQuery(try_take_el[1]);
           if(element.is(':radio') || element.is(':checkbox'))
               value =  jQuery(try_take_el[1]+':checked').val();
           else
               value = element.val();
       }
       return value;
    };
    $this.compare = function (str) {
        var result = !!($this.get_val(str));
        var reg = compare_reg.exec(str);
        if (!reg)
            return result;
        var type = reg[0];
        var compares = str.split(type);
        type = type.trim('{}');
        return compare[type](compares[0], compares[1]);
    };
    $this.match = function (str) {
        var check, type, cr_type, temp, result = $this.compare(str), max_for = str.length, wrap = '{split}';
        for (var i = 0; i < max_for; i++) {
            check = match_reg.exec(str);
            if (!check) {
                if (i > 0)
                    result = match[cr_type](result, str);
                break;
            }
            type = check[0].trim('{}');
            str = str.replace(check[0], wrap);
            check = str.split(wrap);
            str = check[1];
            temp = check[0];
            if (i === 0)
                result = temp;
            else
                result = match[cr_type](result, temp);
            cr_type = type;
        }
        return result;
    };
    // abcd = xyz && yzk = asd
};
EF4Math = function () {
    var $this = this;
    var math_reg = new RegExp('[a-z]+:{[a-zA-Z0-9:,.-]+}');
    var compare_reg = new RegExp('{[!<>=]+}');
    var match_reg = new RegExp('{[&|]+}');
    var calculator = {
        'mul': function (a, b) {
            return parseFloat(a) * parseFloat(b);
        },
        'sum': function (a, b) {
            return parseFloat(a) + parseFloat(b);
        },
        'div': function (a, b) {
            return parseFloat(a) / parseFloat(b);
        },
        'sub': function (a, b) {
            return parseFloat(a) - parseFloat(b);
        }
    };
    var compare = {
        '>': function (a, b) {
            return $this.math(a) > $this.math(b);
        },
        '>=': function (a, b) {
            return $this.math(a) >= $this.math(b);
        },
        '<': function (a, b) {
            return $this.math(a) < $this.math(b);
        },
        '<=': function (a, b) {
            return $this.math(a) <= $this.math(b);
        },
        '!=': function (a, b) {
            return $this.math(a) != $this.math(b);
        },
        '=': function (a, b) {
            return $this.math(a) == $this.math(b);
        }
    };
    var match = {
        '&&': function (a, b) {
            return !!($this.compare(a) && $this.compare(b));
        },
        '||': function (a, b) {
            return !!($this.compare(a) || $this.compare(b));
        }
    };

    this.math = function (str) {
        if (!str)
            return 0;
        var rs, elements, type, result, max_for = str.length;
        for (var i = 0; i < max_for; i++) {
            if (!isNaN(str))
                break;
            rs = math_reg.exec(str);
            if (!rs)
                break;
            rs = rs[0];
            type = rs.split(':')[0];
            elements = rs.substr(0, rs.length - 1).substr(5).split(',');
            elements.forEach(function (item, index) {
                if (isNaN(item)) {
                    var nodes = document.querySelectorAll('.math-group[data-name*="' + item + '"]');
                    item = (nodes.length > 0) ? nodes[0].value : 0;
                }
                if (index === 0)
                    result = item;
                else
                    result = calculator[type](result, item);
            });
            str = str.replace(rs, result);
        }
        if (isNaN(str)) {
            //try take value
            var nodes = document.querySelectorAll('.math-group[data-name*="' + str + '"]');
            str = (nodes.length > 0) ? nodes[0].value : 0;
        }
        if (isNaN(str))
            str = 0;
        return Number((parseFloat(str)).toFixed(2));
    };
    this.compare = function (str) {
        var result = !!($this.math(str));
        var reg = compare_reg.exec(str);
        if (!reg)
            return result;
        var type = reg[0];
        var compares = str.split(type);
        type = type.trim('{}');
        return compare[type](compares[0], compares[1]);
    };
    this.match = function (str) {
        var check, type, cr_type, temp, result = $this.compare(str), max_for = str.length, wrap = '{split}';
        for (var i = 0; i < max_for; i++) {
            check = match_reg.exec(str);
            if (!check) {
                if (i > 0)
                    result = match[cr_type](result, str);
                break;
            }
            type = check[0].trim('{}');
            str = str.replace(check[0], wrap);
            check = str.split(wrap);
            str = check[1];
            temp = check[0];
            if (i === 0)
                result = temp;
            else
                result = match[cr_type](result, temp);
            cr_type = type;
        }
        return result;
    }
};
jQuery(document).ready(function ($) {
    var $document = $(document), cal = new EF4Math(),dp = new EF4Dependency();
    var dependency_attach_attr = 'data-d-attach',dependency_id_attr = 'data-d-id',dependency_selector= '.ef4-dependency'
        ,dependency_match_attr = 'data-match';
    $document.on('ef4.dependency.init',function () {
        $document.find(dependency_selector+':not(['+dependency_id_attr+'])').each(function () {
             var $this = $(this),id = rand_str();
            $this.attr(dependency_id_attr,id);
            dp.get_attach_element_selector($this.attr(dependency_match_attr)).forEach(function (item) {
                attach_dependency_id(item,id);
            });
        });
        $document.find(dependency_selector+'['+dependency_match_attr+']').each(function () {
            check_dependency_match($(this));
        });
    }).on('change','['+dependency_attach_attr+']',function () {
        var attach = $(this).attr(dependency_attach_attr);
        var attach_arr = (attach) ? attach.split(',') : [];
        attach_arr.forEach(function (item) {
            var target = $(dependency_selector+'['+dependency_id_attr+'="'+recover_attach_mask(item)+'"]');
            if(target.length < 1)
                return;
            check_dependency_match(target);
        })
    });
    function check_dependency_match(target) {
        if(dp.match(target.attr(dependency_match_attr)))
            target.show();
        else
            target.hide();
    }
    function attach_dependency_id(el_selector,id) {
        var target = $(el_selector),mask = get_attach_mask(id);
        var attach = target.attr(dependency_attach_attr);
        var attach_arr = (attach) ? attach.split(',') : [];
        if(attach_arr.indexOf(mask) == -1)
            attach_arr.push(mask);
        target.attr(dependency_attach_attr,attach_arr.join(','));
    }
    function get_attach_mask(id)
    {
        return '{'+id+'}';
    }
    function recover_attach_mask(mask) {
        return mask.substr(1,mask.length -2);
    }
    function rand_str(len) {
        if(!len)
            len = 8;
        var text = "";
        var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        var rand;
        for (var i = 0; i < len; i++)
        {
            rand = Math.floor( Math.random() * possible.length);
            if(rand >= possible.length)
                rand = possible.length -1;
            text += possible.charAt(rand);
        }

        return text;
    }

    //other api
    var form_selector = 'form';
    $document.on('click', '.button.radio-group', function () {
        var $this = $(this), form = $this.closest(form_selector),
            group = $this.attr('data-group'), connect = $this.attr('data-connect'), value = $this.attr('data-value');
        if (!group || !connect) return;
        form.find('.button.radio-group[data-group="' + group + '"]').removeClass('active');
        $this.addClass('active');
        form.find('[name="' + connect + '"]').val(value).change();
    }).on('change', '.connect-group', function () {
        var $this = $(this), class_list = $this.attr('class').split(' '), group_connect = [], form = $this.closest(form_selector);
        class_list.forEach(function (item) {
            if (item.indexOf('group-') === 0) {
                group_connect.push(item.substr('group-'.length));
            }
        });
        group_connect.forEach(function (item) {
            form.find('[data-group="' + item + '"]').removeClass('active');
            form.find('[data-group="' + item + '"][data-value="' + $this.val() + '"]').addClass('active');
        })
    });
    //end other api
    $document.on('show','.view-single',function () {
        on_trigger_show_view(this);
    }).on('ef4.view.show','.view-single',function () {
        on_trigger_show_view(this);
    }).on('ef4.view.initial','div',function (e) {
        var $this = $(this);
        $this.find('.view-single.view-initial').each(function () {
            show_single_view($(this).attr('data-name'),{show_mode:'none',hide_mode:'none',container:$this});
        });
        // show_single_view($(this).attr('data-name'),{show_mode:'none',hide_mode:'none'});
    }).on('click', '.view-trigger', function (e) {
        var $this = $(this), show = $this.attr('data-show'),
            show_mode = $this.attr('data-show-mode'), hide_mode = $this.attr('data-hide-mode');
        if ($this.is('a')) e.preventDefault();
        show_single_view(show,{show_mode:show_mode,hide_mode:hide_mode});
    }).on('change','.view-input-state',function () {
        var $this = $(this), show = $this.val(),show_mode = $this.attr('data-show-mode'), hide_mode = $this.attr('data-hide-mode');
        show_single_view(show,{show_mode:show_mode,hide_mode:hide_mode});
    });
    function on_trigger_show_view(el)
    {
        var $el = $(el),container = $el.closest('.view-container'),options = {show_mode:'none',hide_mode:'none'},name = $el.attr('data-name');
        if(container.is('.view-container'))
            options['container'] = container;
        show_single_view(name,options);
    }
    function show_single_view(name,options) {
        if(!name)
            return;
        var show_e = $('.view-single[data-name="' + name + '"]');
        var group = show_e.attr('data-group');
        var show_mode = (options && options['show_mode']) ? options['show_mode'] : '';
        var hide_mode = (options && options['hide_mode'] ) ? options['hide_mode'] : '';
        var container = (options && (options['container'] instanceof jQuery)) ? options['container'] : $document;
        var hide_e = container.find('.view-single[data-group="'+group+'"]:not([data-name="' + name + '"])');
        switch (show_mode) {
            default:
            case 'slide':
                show_e.slideDown();
                break;
            case 'fade':
                show_e.fadeIn();
                break;
            case 'none':
                break;
        }
        show_e.addClass('active');
        switch (hide_mode) {
            default:
            case 'slide':
                hide_e.slideUp();
                break;
            case 'fade':
                hide_e.fadeOut();
                break;
            case 'none':
                hide_e.css('display', '');
                break;
        }
        hide_e.removeClass('active');
    }
    $document.on('ef4.math.cal', function () {
        $document.find('.math-group.math-element').change();
    });
    var count_change = 0, limit_math = 1000000;
    $document.on('change', '.math-group.math-element', function () {
        count_change++;
        if (count_change == limit_math)
            alert('Maybe infinity loop,break process.');
        if (count_change > 1000000) {
            return;
        }
        var $this = $(this), name = $this.attr('data-name');
        $document.find('.math-group.math-result[data-math*="' + name + '"]').each(function () {
            var $this = $(this);
            cal_set_val($this, $this.attr('data-math'));
        });
        $document.find('.math-group.math-dependency[data-match*="' + name + '"]').each(function () {
            var $this = $(this);
            (cal.match($this.attr('data-match'))) ? $this.show() : $this.hide();
        });
    }).on('click', '.math-group.math-force-value[data-target][data-value]', function () {
        var $this = $(this);
        var target = $('.math-group[data-name="' + $this.attr('data-target') + '"]');
        cal_set_val(target, $this.attr('data-value'));
    });
    function cal_set_val($el, val) {
        var value = cal.math(val), wrap = $el.attr('data-value-wrap');
        if (wrap)
            value = wrap.split('{-value-}').join(value);
        if ($el.is('input') || $el.is('select'))
            $el.val(value).change();
        else
            $el.html(value);
    }

    function init_data_dependency() {
        // el{=>val}{=}
        // el{.div[]=>is|:checked}{=}abc{&&}1{=}
        $document.find('ef4-dependency[data-match]').each(function () {
            var $this = $(this);

        });
    }
});