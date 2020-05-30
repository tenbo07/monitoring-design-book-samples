<template>
  <v-card
    class="mx-auto"
  >
    <v-app-bar
      dark
      :color="configs[columnType].color"
    >
      <v-toolbar-title id="title">{{configs[columnType].name}}</v-toolbar-title>
      <v-spacer></v-spacer>
      <NewTaskDialog></NewTaskDialog>
    </v-app-bar>

    <v-container>
      <v-row dense>
        <v-col
          v-for="(item, i) in taskList"
          :key="i"
          cols="12"
        >
          <TaskCard :item="item" :cardOption="configs[columnType].cardOption"></TaskCard>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>
<script>
  import { mapActions } from "vuex";
  import NewTaskDialog from '@/components/NewTaskDialog.vue'
  import TaskCard from '@/components/TaskCard.vue'

  export default {
    props: {
      columnType: {
        type: String,
        required: true
      },
      taskList: {
        type: Array,
        required: true
      }
    },
    components: {
      NewTaskDialog,
      TaskCard
    },
    data: () => ({
      configs: {
        TODO: {
          name: "TODO",
          color: "#0033cc",
          cardOption: {
            delete: true,
            nextStatus: "inprogress",
            updateBtnName: "Go to In Progress"
          }
        },
        INPROGRESS: {
          name: "In Porogress",
          color: "#cccc00",
          cardOption: {
            delete: true,
            nextStatus: "done",
            updateBtnName: "Go to Done"
          }
        },
        DONE: {
          name: "Done",
          color: "#cc0000",
          cardOption: {
            delete: true,
            nextStatus: "",
          }
        }
      }
    })
  };
</script>
