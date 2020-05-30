<template>
  <div>
    <v-dialog
      v-model="taskUpdating"
      hide-overlay
      persistent
      width="300"
    >
      <v-card
        color="white"
      >
        <v-card-text>
          Updating....
          <v-progress-linear
            indeterminate
            color="primary"
            class="mb-0"
          ></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
    <v-card
      color="#006666"
      dark
    >
      <div class="d-flex flex-no-wrap justify-space-between">
        <v-container>
          <v-card-title
            class="headline"
          >
            <span class="title font-weight-light">{{item.title}}</span>
            <v-spacer></v-spacer>
            <v-btn v-if="cardOption.delete" icon @click="deleteTask(item.task_id)"><v-icon>mdi-delete</v-icon></v-btn>
          </v-card-title>

          <v-card-subtitle v-text="item.description"></v-card-subtitle>
          <v-chip class="ma-2" color="red">{{item.due_date}}</v-chip>

          <v-card-actions v-if="cardOption.nextStatus">
            <v-btn text @click="updateStatus(item.task_id, cardOption.nextStatus)">{{cardOption.updateBtnName}}</v-btn>
          </v-card-actions>
        </v-container>
      </div>
    </v-card>
  </div>
</template>
<script>
  import { mapActions } from "vuex";
  export default {
    props: {
      cardOption:{
        type: Object,
        required: true
      },
      item: {
        type: Object,
        required: true
      }
    },
    data: () => ({
      taskUpdating: false
    }),
    methods: {
      ...mapActions({
        fetchList: "tasks/fetchList"
      }),
      async updateStatus(taskId, status){
        this.taskUpdating = true
        let payload = {
          'task_id': taskId,
          'status': status
        }
        await this.$store.dispatch('tasks/updateTaskStatus', payload)
        await this.fetchList();
        this.taskUpdating = false
      },
      async deleteTask(taskId){
        this.taskUpdating = true
        let payload = {
          'task_id': taskId
        }
        await this.$store.dispatch('tasks/deleteTask', payload)
        await this.fetchList();
        this.taskUpdating = false
      }
    }
  };
</script>
