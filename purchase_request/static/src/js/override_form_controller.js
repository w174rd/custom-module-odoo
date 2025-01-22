/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";

// Apply a patch to FormController
patch(FormController.prototype, {
    async discard() {
        console.log("================="+" custom discard");

        // Call the original discard method
        await super.discard(...arguments);

        try {
            history.back();  
        } catch (error) {
                console.error('Error triggering action:', error);
        }
    },
});