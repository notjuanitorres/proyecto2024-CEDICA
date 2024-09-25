
document.addEventListener('DOMContentLoaded', () => {
  (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
    const $notification = $delete.parentNode;
    const time = 5000; // Time in milliseconds 

    setTimeout(() => {
      if ($notification.parentNode) {
        $notification.parentNode.removeChild($notification);
      }
    }, time);

    // Add click event to delete the notification immediately
    $delete.addEventListener('click', () => {
      if ($notification.parentNode) {
        $notification.parentNode.removeChild($notification);
      }
    });
  });
});