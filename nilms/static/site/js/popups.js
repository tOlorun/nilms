/**
 * implementation example:
 *
 * <div class='popups-container'>
 *     <div class='popups-container-popup' data-name='popup-mail'>
 *          <!-- whatever goes here -->
 *     </div>
 *
 *     <!-- ... can be multiple popups -->
 * </div>
 */
var PopupManagerConfig = {
    'lang': {
        'viewText': 'Visa'
    }
}


var Popup = function(element) {
    var _this = this;

    _this.element = element;
    _this.dataName = null;

    if (_this.element.getAttribute('data-name'))
        _this.dataName = _this.element.getAttribute('data-name');

    /**
     * When the popup is clicked
     */
    _this.handleClick = function(e) {
        e.stopPropagation();

        return false;
    }

    _this.activate = function() {
        _this.element.setAttribute('data-active', true);
    };

    _this.deactivate = function() {
        _this.element.setAttribute('data-active', false);
    };

    _this.isActive = function() {
        return _this.element.getAttribute('data-active') == 'true';
    }

    _this.isTemporary = function() {
        return _this.element.getAttribute('data-temp') == 'true';
    }

    _this.toggle = function() {
        if (_this.isActive())
            _this.deactivate();
        else
            _this.activate();
    };


    _this.element.setAttribute('data-active', false);
    _this.element.addEventListener('click', _this.handleClick);
}


var PopupManager = function(element) {
    var _this = this;

    _this.element = element;
    _this.popupElements = element.querySelectorAll('.popups-container-popup');
    _this.popups = [];

    _this.element.setAttribute('data-active', false);

    /**
     * When the container is clicked
     */
    _this.handleClick = function(e) {
        e.stopPropagation();

        _this.toggle();

        for (var i = 0; i < _this.popups.length; i++)
            if (_this.popups[i].isActive())
                _this.popups[i].deactivate();

        return false;
    }

    _this.activate = function() {
        _this.element.setAttribute('data-active', true);
    };

    _this.deactivate = function() {
        _this.element.setAttribute('data-active', false);

        for (var i = 0; i < _this.popups.length; i++)
            if (_this.popups[i].isTemporary()) {
                _this.element.removeChild(_this.popups[i].element);
                _this.popups.pop(_this.popups[i]);
            }
    };

    _this.isActive = function() {
        return _this.element.getAttribute('data-active') == 'true';
    }

    _this.toggle = function() {
        if (_this.isActive())
            _this.deactivate();
        else
            _this.activate();
    };

    _this.showInformationPopup = function(description, href, name) {
        var popupElement = document.createElement('div');
        popupElement.className += ' popups-container-popup';
        popupElement.setAttribute('data-name', name);
        popupElement.setAttribute('data-temp', true);

        var popupContentElement = document.createElement('div');
        popupContentElement.className += ' popup-content';
        popupContentElement.innerHTML = atob(description);

        var popupElementButton = document.createElement('a');
        popupElementButton.className += ' button button-primary';
        popupElementButton.setAttribute('href', href);
        popupElementButton.innerHTML = PopupManagerConfig.lang.viewText;

        popupContentElement.appendChild(popupElementButton);
        popupElement.appendChild(popupContentElement);


        _this.element.appendChild(popupElement);

        var pop = new Popup(popupElement);

        _this.popups.push(pop);

        _this.toggle();
        pop.toggle();
    };

    for (var i = 0; i < _this.popupElements.length; i++)
        _this.popups.push(new Popup(_this.popupElements[i]));

    _this.getPopup = function(popupName) {
        for (var i = 0; i < _this.popups.length; i++)
            if (_this.popups[i].dataName == popupName)
                return _this.popups[i];
    };
    
    _this.togglePopup = function(popupName) {
        _this.toggle();
        _this.getPopup(popupName).toggle();
    };


    _this.element.addEventListener('click', _this.handleClick);
}



document.addEventListener('DOMContentLoaded', function(e) {
    var popup_container = document.querySelector('.popups-container');

    if (popup_container == null)
        return;

    window.popupManager = new PopupManager(popup_container);
});
