/**
 * Created by Admin on 7/2/2018.
 */
jQuery(document).ready(function ($) {
    var form_trigger = '.ef4-payments-trigger[data-target]', form_selector = '.ef4-payment-form';
    $(document).on('click', form_trigger, function (e) {
        var $this = $(this);
        if ($this.is('a'))
            e.preventDefault();
        show_form($this.attr('data-target'), $this.attr('data-options'));
    }).on('submit', form_selector + ' form', function (e) {
        e.preventDefault();
        submit_form($(this));
    }).on('click',form_selector + ' .form-close',function (e) {
        e.preventDefault();
        close_form(this);
    });
    var ajax_save_running;
    function close_form(el) {
        var $el = $(el);
        var modal = $el.closest(form_selector);
        if(!modal.is('.modal'))
            modal = modal.closest('.modal');
        modal.modal('hide');
    }
    function submit_form(form) {
        var data = {
            data: get_input_data(form, '[name]'),
            action: ef4_payments['settings']['action'],
            nonce: ef4_payments['settings']['nonce']
        };
        ajax_save_running = true;
        var form_container =  form.closest(form_selector);
        form_container.find('.view-single[data-name="payment-loading"]').trigger('show');
        $.ajax({
            type: "POST",
            url: ef4_payments['settings']['ajaxurl'],
            data: data,
            success: function (response) {
                render_response_payment_form(response,form);
            },
            dataType: 'JSON'
        }).fail(function () {
            form_container.find('.view-single[data-name="payment-fail"]').trigger('show');
        }).always(function () {
            ajax_save_running = false;
        });
    }
    function render_response_payment_form(response,form) {
        var container = (form.is(form_selector)) ? form : form.closest(form_selector);
        switch (response['status'])
        {
            case 'success':
                var result_container = container.find('.view-single[data-name="payment-result"]');
                result_container.html(response['message']);
                if(response['action'] && typeof response['action'] == 'object')
                {
                    do_extend_action(response['action']);
                }
                extends_modify_view(result_container);
                result_container.trigger('show');
                break;
            case 'fail':
                var fail_container = container.find('.view-single[data-name="payment-fail"]');
                fail_container.html = response['message'];
                if(typeof response['action'] == 'object')
                {
                    do_extend_action(response['action']);
                }
                fail_container.trigger('show');
                break;
        }
       
    }
    function extends_modify_view(view) {
        view.find('.show-if-match').each(function () {
           var $this= $(this),match = $this.attr('data-match'),check = $this.attr('data-check');
           if(match == check)
               $this.show();
           else
               $this.hide();
        });
        view.find('.hidden-if-empty[data-check=""]').hide();
    }
    function do_extend_action(action) {
        if(typeof action != 'object')
            return;
        switch (action['type'])
        {
            case 'redirect':
                var delay = (action['data']['delay']) ? parseInt(action['data']['delay'])*1000 : 100 ;
                setTimeout(function () {
                    window.location = action['data']['url'];
                },delay);
                break;
        }
    }
    function show_form(target, item) {
        var form = $(form_selector + '[data-target="' + target + '"]');
        var data = ef4_payments['items'][target][item];
        if (!data)
            return;
        var items_id = [];
        form.find('.dynamic-element').remove();
        form.find('.dynamic-data').each(function () {
            var $this = $(this), element = $this.attr('data-target'),
                template = $this.attr('data-template'), mode = $this.attr('data-insert-mode'),
                cr_el, k, cr_template ,special_key = 'special', special_prefix = special_key+':';
            if(element.indexOf(special_prefix) != -1)
            {
                //handle for special field;
                var sp_key = element.substr(special_prefix.length);
                var current_val = data[special_key][sp_key];
                if(!current_val)
                    return;
                for(var key in current_val)
                {
                    if(current_val.hasOwnProperty(key))
                    {
                        cr_template = template;
                        cr_template = replace_data(cr_template, {key:key,value:current_val[key]});
                        cr_template = $(cr_template).addClass('dynamic-element');
                        switch (mode) {
                            case 'after':
                                cr_template.insertAfter($this);
                                break;
                            default:
                                $this.append(cr_template);
                        }
                    }
                }
                return;
            };
            if (!data[element])
                return;
            for (k in data[element]) {
                if (!data[element].hasOwnProperty(k))
                    continue;
                if (element == 'items' && items_id.indexOf(k) === -1)
                    items_id.push(k);
                cr_el = data[element][k];
                cr_template = template;
                cr_template = replace_data(cr_template, cr_el);
                cr_template = $(cr_template).addClass('dynamic-element');
                switch (mode) {
                    case 'after':
                        cr_template.insertAfter($this);
                        break;
                    default:
                        $this.append(cr_template);
                }
            }
        });
        form.find('.dynamic-attr').each(function () {
            var $this = $(this), options = json_tryparse($this.attr('data-options'))
                , attr, items, value, k, el, seg, join, wrap;
            for (attr in options) {
                if (!options.hasOwnProperty(attr))
                    continue;
                el = options[attr]['elements'];
                seg = options[attr]['segment'];
                join = options[attr]['join'];
                wrap = options[attr]['wrap'];
                if (!el || !data[el] || !seg)
                    continue;
                items = data[el];
                value = [];
                for (k in items) {
                    if (!items.hasOwnProperty(k))
                        continue;
                    value.push(replace_data(seg, items[k]));
                    if (!join)
                        break;
                }
                if (wrap)
                    value = wrap.split('{-value-}').join(value.join(join));
                else
                    value = value.join(join);
                $this.attr(attr, value);
            }
        });

        $(document).trigger('ef4.math.cal');

        var payment_required_fields = {
            'form-type': data['settings']['form_type'],
            'form-item-source': data['settings']['form_item_source'],
            'form-items': items_id.join(','),
            'form-request-url':window.location.toString()
        };
        for (var name in payment_required_fields)
            if (payment_required_fields.hasOwnProperty(name)) {
                if (form.find('form [name="' + name + '"]').length < 1)
                    form.find('form').append('<input type="hidden" name="' + name + '">')
                form.find('form [name="' + name + '"]').val(payment_required_fields[name]);
            }
        form.trigger('ef4.view.initial');
        form.modal();
    }

    function get_input_data(container, mask) {
        if (!mask) mask = 'input-field';
        var data = {};
        container.find(mask).each(function () {
            var $this = jQuery(this);
            if (!$this.attr('name')) return;
            if ($this.is(':checkbox')) {
                data[$this.attr('name')] = ($this.is(':checked')) ? 'yes' : 'no';
            } else if ($this.is(':radio')) {
                if ($this.is(':checked'))
                    data[$this.attr('name')] = $this.val();
            }
            else {
                data[$this.attr('name')] = $this.val();
            }
        });
        return data;
    }

    function replace_data(str, data) {
        for (var k in data) {
            if (!data.hasOwnProperty(k))
                continue;
            str = str.split('{{_' + k + '_}}').join(data[k]);
        }
        return str;
    }

    function json_tryparse(str) {
        var result = {};
        try {
            result = JSON.parse(str)
        }
        catch (e) {
            result = {}
        }
        return result;
    }
});