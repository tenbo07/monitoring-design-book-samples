var synthetics = require('Synthetics');

const ToDoAppGUIFlow = async function () {

    let appURL = "<Your App URL>";
    let page = await synthetics.getPage();

    // Open Top Page
    await synthetics.executeStep('LoadingTopPage', async function (timeoutInMillis = 30000) {
        await page.goto(appURL, {waitUntil: ['load', 'networkidle0'], timeout: timeoutInMillis});
    });

    // Add New Task
    await synthetics.executeStep('AddNewTask', async function () {
      let taskTitle = "task-" + Math.random().toString(36).substring(7);
      await page.waitForSelector("#new-task-button", { timeout: 30000 });
      await page.click("#new-task-button");
      await page.waitForSelector("#new-task-dialog", { timeout: 30000 });
      await page.type("#new-task-name", taskTitle);
      await page.type("#new-task-desp", "Task Description");
      await page.type("#new-task-due-date", "2020-05-03");
      try {
          await synthetics.takeScreenshot("input-task", 'result');
      } catch(ex) {
          synthetics.addExecutionError('Unable to capture screenshot.', ex);
      }
      await Promise.all([
          page.click("#register-new-task"),
          page.waitForSelector('#new-task-dialog-card', {hidden: true})
      ]);
    });
};

// Handler
exports.handler = async () => {
    return await ToDoAppGUIFlow();
};