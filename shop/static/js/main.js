(($) => {

    class Toggle {
  
      constructor(element, options) {
  
        this.defaults = {
          icon: 'fa-eye'
        };
  
        this.options = this.assignOptions(options);
  
        this.$element = element;
        this.$button = $(`<span class="btn-toggle-pass"> <i class="fa ${this.options.icon}"></i><span>`);
  
        this.init();
      };
  
      assignOptions(options) {
        return $.extend({}, this.defaults, options);
      }
  
      init() {
        this._appendButton();
        this.bindEvents();
      }
  
      _appendButton() {
        this.$element.after(this.$button);
      }
  
      bindEvents() {
  
        this.$button.on('click touchstart', this.handleClick.bind(this));
      }
  
      handleClick() {
  
        let type = this.$element.attr('type');
  
        type = type === 'password' ? 'text' : 'password';
  
        this.$element.attr('type', type);
        this.$button.toggleClass('active');
      }
    }
  
    $.fn.togglePassword = function (options) {
      return this.each(function () {
        new Toggle($(this), options);
      });
    }
  
  })(jQuery);
  
  $(document).ready(function() {
    $('#password').togglePassword();

  })

