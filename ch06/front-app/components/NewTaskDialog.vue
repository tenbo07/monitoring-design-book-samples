<template>
  <v-dialog v-model="dialog" persistent max-width="600px" id="new-task-dialog">
    <template v-slot:activator="{ on }">
      <v-btn icon v-on="on" id="new-task-button" ><v-icon>mdi-plus</v-icon></v-btn>
    </template>
    <v-card id="new-task-dialog-card" :loading="submitting" >
      <v-card-title>
        <span class="headline">New Task</span>
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field label="Task Name" v-model="newTask.title" id="new-task-name" required></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field label="Descriptions" v-model="newTask.description" id="new-task-desp" required></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-menu
                ref="menu"
                v-model="menu"
                :close-on-content-click="false"
                transition="scale-transition"
                offset-y
                min-width="290px"
              >
                <template v-slot:activator="{ on }">
                  <v-text-field
                    v-model="newTask.due_date"
                    label="Input Due Date"
                    prepend-icon="mdi-calendar"
                    readonly
                    v-on="on"
                    id="new-task-due-date"
                  ></v-text-field>
                </template>
                <v-date-picker v-model="newTask.due_date" @input="menu = false"></v-date-picker>
              </v-menu>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="grey" outlined @click="dialog = false">Cancel</v-btn>
        <v-btn color="primary" dark @click="submit" id="register-new-task">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
  import { mapActions, mapGetters } from "vuex";

  export default {
    data: () => ({
      dialog: false,
      submitting: false,
      menu: false,
      newTask: {
        title: "",
        description: "",
        due_date: new Date().toISOString().substr(0, 10)
      }
    }),
    methods: {
      ...mapActions({
        fetchList: "tasks/fetchList"
      }),
      async submit(){
        this.submitting = true
        console.log(this.newTask)
        await this.$store.dispatch('tasks/postNewTask', this.newTask)
        await this.fetchList();
        this.submitting = false
        this.dialog = false
      }
    }
  }
</script>
