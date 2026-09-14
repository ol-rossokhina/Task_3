from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

_DRAG_AND_DROP_JS = """
function simulateDragDrop(sourceNode, destinationNode) {
    function createCustomEvent(type) {
        var event = new CustomEvent("CustomEvent");
        event.initCustomEvent(type, true, true, null);
        event.dataTransfer = {
            data: {},
            setData: function (type, val) {
                this.data[type] = val;
            },
            getData: function (type) {
                return this.data[type];
            },
        };
        return event;
    }

    function dispatchEvent(node, type, event) {
        if (node.dispatchEvent) {
            return node.dispatchEvent(event);
        }
    }

    var dragStartEvent = createCustomEvent("dragstart");
    dispatchEvent(sourceNode, "dragstart", dragStartEvent);

    var dropEvent = createCustomEvent("drop");
    dropEvent.dataTransfer = dragStartEvent.dataTransfer;
    dispatchEvent(destinationNode, "drop", dropEvent);

    var dragEndEvent = createCustomEvent("dragend");
    dragEndEvent.dataTransfer = dragStartEvent.dataTransfer;
    dispatchEvent(sourceNode, "dragend", dragEndEvent);
}
simulateDragDrop(arguments[0], arguments[1]);
"""


def drag_and_drop(driver: WebDriver, source: WebElement, target: WebElement) -> None:
    """Перетаскивает source на target, эмулируя нативные HTML5 DnD-события."""
    driver.execute_script(_DRAG_AND_DROP_JS, source, target)
